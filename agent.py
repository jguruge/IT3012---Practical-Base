from collections import defaultdict
from collections import deque
import heapq
import math
from tracemalloc import start

def bfs_search(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order 

def dfs_search(graph, start):
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)

            for neighbor in reversed(graph.get(vertex, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return result

def ucs_search(graph, start, goal):
    priority_queue = [(0, start, [start])]
    explored = set()
    
    while priority_queue:
        current_cost, current_node, path = heapq.heappop(priority_queue)
        
        if current_node in explored:
            continue
        explored.add(current_node)

        if current_node == goal:
            return current_cost, path
        
        for neighbor, edge_cost in graph.get(current_node, []):
            if neighbor not in explored:
                new_total_cost = current_cost + edge_cost
                
                heapq.heappush(priority_queue, (new_total_cost, neighbor, path + [neighbor]))
    
    return None, None   

class SimpleReflexAgent:
    def sense_and_act(self, percept):
        if percept.get('food_here'):
            return 'suck'
        elif percept.get('wall_ahead'):
            return 'turn_left'
        else:
            return 'move_forward'


class ModelBasedAgent:
    def __init__(self):
        self.visit_counts = defaultdict(int)
        self.known_walls = set()
        self.current_pos = (0, 0)
        self.facing = 'Up'
        self.last_action = None

    def get_visit_count(self, cell):
        if cell in self.known_walls:
            return 999999
        return self.visit_counts[cell]

    def sense_and_act(self, percept):
        dirs = ['Up', 'Right', 'Down', 'Left']
        dir_offsets = {
            'Up': (0, 1),
            'Right': (1, 0),
            'Down': (0, -1),
            'Left': (-1, 0)
        }

        if self.last_action == 'turn_left':
            idx = dirs.index(self.facing)
            self.facing = dirs[(idx - 1) % 4]
        elif self.last_action == 'turn_right':
            idx = dirs.index(self.facing)
            self.facing = dirs[(idx + 1) % 4]
        elif self.last_action == 'move_forward':
            dx, dy = dir_offsets[self.facing]
            self.current_pos = (self.current_pos[0] + dx, self.current_pos[1] + dy)

        self.visit_counts[self.current_pos] += 1

        idx = dirs.index(self.facing)
        front_dir = dirs[idx]
        left_dir = dirs[(idx - 1) % 4]
        right_dir = dirs[(idx + 1) % 4]

        fx, fy = dir_offsets[front_dir]
        lx, ly = dir_offsets[left_dir]
        rx, ry = dir_offsets[right_dir]

        front_cell = (self.current_pos[0] + fx, self.current_pos[1] + fy)
        left_cell = (self.current_pos[0] + lx, self.current_pos[1] + ly)
        right_cell = (self.current_pos[0] + rx, self.current_pos[1] + ry)

        if percept.get('wall_ahead'):
            self.known_walls.add(front_cell)

        if percept.get('food_here'):
            action = 'suck'
        elif percept.get('wall_ahead'):
            left_count = self.get_visit_count(left_cell)
            right_count = self.get_visit_count(right_cell)
            if left_count < right_count:
                action = 'turn_left'
            else:
                action = 'turn_right'
        else:
            front_count = self.get_visit_count(front_cell)
            left_count = self.get_visit_count(left_cell)
            right_count = self.get_visit_count(right_cell)

            if front_count == 0:
                action = 'move_forward'
            elif left_count == 0:
                action = 'turn_left'
            elif right_count == 0:
                action = 'turn_right'
            else:
                min_count = min(front_count, left_count, right_count)
                if min_count == front_count:
                    action = 'move_forward'
                elif min_count == left_count:
                    action = 'turn_left'
                else:
                    action = 'turn_right'

        self.last_action = action
        return action


class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'
        self.current_pos = (0, 0)

    def manhattan_distance(self, pos, goal):
        return int(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))

    def euclidean_distance(self, pos, goal):
        return float(math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2))

    def sense_and_act(self, percept):
        if percept.get('food_here'):
            return 'suck'
            
        if not self.plan:
            all_food = percept.get('all_food', [])
            if not all_food:
                return 'suck'  # Default action
                
            walls = percept.get('walls', [])
            grid_size = percept.get('grid_size', (10, 10))
            
            # Sort food by Manhattan distance to self.current_pos
            sorted_food = sorted(all_food, key=lambda f: abs(f[0] - self.current_pos[0]) + abs(f[1] - self.current_pos[1]))
            
            path = None
            for food in sorted_food:
                if self.active_algo == 'BFS':
                    path = self.bfs_search(self.current_pos, food, walls, grid_size)
                elif self.active_algo == 'DFS':
                    path = self.dfs_search(self.current_pos, food, walls, grid_size)
                elif self.active_algo == 'UCS':
                    path = self.ucs_search(self.current_pos, food, walls, grid_size)
                elif self.active_algo == 'AStar':
                    remaining_food = percept.get('remaining_food', len(all_food))
                    path = self.astar_search(self.current_pos, food, walls, grid_size, heuristic_type='manhattan')
                
                if path is not None and len(path) > 0:
                    self.plan = list(path)
                    break
            
            if not self.plan:
                return 'suck'  # Default action if no reachable food
                
        action = self.plan.pop(0)
        
        # Update agent's internal position estimate
        dx, dy = 0, 0
        if action == 'Up':
            dy = 1
        elif action == 'Down':
            dy = -1
        elif action == 'Left':
            dx = -1
        elif action == 'Right':
            dx = 1
        self.current_pos = (self.current_pos[0] + dx, self.current_pos[1] + dy)
        
        return action

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        """
        Breadth-First Search (BFS) explores the shallowest nodes first.
        Uses a FIFO queue (deque.popleft()).
        """
        width, height = grid_size
        walls_set = set(walls)
        
        if start_pos == goal_pos:
            return []
            
        queue = deque([(start_pos, [])])
        reached = {start_pos}
        
        directions = [
            ('Up', (0, 1)),
            ('Right', (1, 0)),
            ('Down', (0, -1)),
            ('Left', (-1, 0))
        ]
        
        while queue:
            curr, path = queue.popleft()
            
            if curr == goal_pos:
                return path
                
            for action, (dx, dy) in directions:
                next_pos = (curr[0] + dx, curr[1] + dy)
                if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                    if next_pos not in walls_set and next_pos not in reached:
                        reached.add(next_pos)
                        queue.append((next_pos, path + [action]))
                        
        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        """
        Depth-First Search (DFS) explores the deepest nodes first.
        Uses a LIFO stack (list.pop()).
        """
        width, height = grid_size
        walls_set = set(walls)
        
        if start_pos == goal_pos:
            return []
            
        stack = [(start_pos, [])]
        reached = set()
        
        directions = [
            ('Up', (0, 1)),
            ('Right', (1, 0)),
            ('Down', (0, -1)),
            ('Left', (-1, 0))
        ]
        
        while stack:
            curr, path = stack.pop()
            
            if curr == goal_pos:
                return path
                
            if curr in reached:
                continue
            reached.add(curr)
            
            for action, (dx, dy) in directions:
                next_pos = (curr[0] + dx, curr[1] + dy)
                if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                    if next_pos not in walls_set and next_pos not in reached:
                        stack.append((next_pos, path + [action]))
                        
        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        """
        Uniform-Cost Search (UCS) uses a Priority Queue (heapq.heappop())
        ordered by the total path cost g(n).
        """
        width, height = grid_size
        walls_set = set(walls)
        
        if start_pos == goal_pos:
            return []
            
        pq = []
        counter = 0
        heapq.heappush(pq, (0, counter, start_pos, []))
        reached = {}  # state -> cheapest cost to reach this state
        
        directions = [
            ('Up', (0, 1)),
            ('Right', (1, 0)),
            ('Down', (0, -1)),
            ('Left', (-1, 0))
        ]
        
        while pq:
            cost, _, curr, path = heapq.heappop(pq)
            
            if curr == goal_pos:
                return path
                
            if curr in reached and reached[curr] <= cost:
                continue
            reached[curr] = cost
            
            for action, (dx, dy) in directions:
                next_pos = (curr[0] + dx, curr[1] + dy)
                if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                    if next_pos not in walls_set:
                        next_cost = cost + 1
                        if next_pos not in reached or next_cost < reached[next_pos]:
                            counter += 1
                            heapq.heappush(pq, (next_cost, counter, next_pos, path + [action]))
                            
        return None

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        """
        A* Search evaluates nodes by combining the path cost g(n) and the estimated cost to the goal h(n).
        Evaluation function: f(n) = g(n) + h(n).
        """
        width, height = grid_size
        walls_set = set(walls)
        
        if start_pos == goal_pos:
            return []
            
        pq = []
        if heuristic_type == 'manhattan':
            h_start = self.manhattan_distance(start_pos, goal_pos)
        else:
            h_start = self.euclidean_distance(start_pos, goal_pos)
            
        heapq.heappush(pq, (h_start, 0, start_pos, []))
        reached_states = set()
        
        directions = [
            ('Up', (0, 1)),
            ('Right', (1, 0)),
            ('Down', (0, -1)),
            ('Left', (-1, 0))
        ]
        
        while pq:
            f_cost, g_cost, curr, path = heapq.heappop(pq)
            
            if curr == goal_pos:
                return path
                
            if curr in reached_states:
                continue
            reached_states.add(curr)
            
            for action, (dx, dy) in directions:
                next_pos = (curr[0] + dx, curr[1] + dy)
                if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                    if next_pos not in walls_set and next_pos not in reached_states:
                        g_new = g_cost + 1
                        if heuristic_type == 'manhattan':
                            h_new = self.manhattan_distance(next_pos, goal_pos)
                        else:
                            h_new = self.euclidean_distance(next_pos, goal_pos)
                        f_new = g_new + h_new
                        heapq.heappush(pq, (f_new, g_new, next_pos, path + [action]))
                        
        return None

if __name__ == '__main__':
    agent = SearchAgent()
    print("Manhattan distance:", agent.manhattan_distance((0, 0), (3, 4)))
    print("Euclidean distance:", agent.euclidean_distance((0, 0), (3, 4)))