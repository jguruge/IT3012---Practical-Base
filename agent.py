# agent.py
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
        self.agent_pos = (0, 0)
        self.alive = True
        self.toxic_traps = []
        self.pit_locations = []
        self.gold_locations = []

    def sense_and_act(self, percept: dict) -> str:
 
        pos = percept['agent_pos']
        
        # STEP 2.2: Rational action selection
        # Priority 1: Avoid toxin
        if percept.get('smells_toxin', False):
            return random.choice(['Left', 'Right', 'Up', 'Down'])
        
        # Priority 2: Grab food if present
        if percept.get('smells_food', False):
            return random.choice(self.actions_pool)
        
        # Priority 3: Explore safely
        return random.choice(self.actions_pool)


#Lab 02
class SimpleReflexAgent:

    def sense_and_act(self, percept):

        if percept['food_here']:
            return 'Right'

        if percept['wall_ahead']:
            return 'Left'

        return 'Right'

# Lab 02
class ModelBasedAgent:

    def __init__(self):
        self.visited_cells = set()  # Tracks actual coordinates visited
        self.walls = set()          # Tracks positions known to be walls
        self.position = (0, 0)      # Transition model: coordinates estimate
        self.last_action = None

    def sense_and_act(self, percept):
        # 1. Update Transition Model (estimated position based on last action taken)
        if self.last_action == 'Up':
            self.position = (self.position[0], self.position[1] + 1)
        elif self.last_action == 'Down':
            self.position = (self.position[0], self.position[1] - 1)
        elif self.last_action == 'Left':
            self.position = (self.position[0] - 1, self.position[1])
        elif self.last_action == 'Right':
            self.position = (self.position[0] + 1, self.position[1])

        # Sensor correction: If a wall was ahead and we tried to move into it, 
        # we didn't actually move. Record the wall position and revert coordinate update.
        if percept['wall_ahead'] and self.last_action in ['Up', 'Down', 'Left', 'Right']:
            if self.last_action == 'Up':
                wall_pos = (self.position[0], self.position[1])
                self.walls.add(wall_pos)
                self.position = (self.position[0], self.position[1] - 1)
            elif self.last_action == 'Down':
                wall_pos = (self.position[0], self.position[1])
                self.walls.add(wall_pos)
                self.position = (self.position[0], self.position[1] + 1)
            elif self.last_action == 'Left':
                wall_pos = (self.position[0], self.position[1])
                self.walls.add(wall_pos)
                self.position = (self.position[0] + 1, self.position[1])
            elif self.last_action == 'Right':
                wall_pos = (self.position[0], self.position[1])
                self.walls.add(wall_pos)
                self.position = (self.position[0] - 1, self.position[1])

        # 2. Record this position in our spatial memory
        self.visited_cells.add(self.position)

        # 3. Query memory and select action
        possible_moves = {
            'Up': (self.position[0], self.position[1] + 1),
            'Down': (self.position[0], self.position[1] - 1),
            'Left': (self.position[0] - 1, self.position[1]),
            'Right': (self.position[0] + 1, self.position[1])
        }

        # Filter out moves that go to already visited coordinates or known walls
        unvisited_moves = [move for move, pos in possible_moves.items() if pos not in self.visited_cells and pos not in self.walls]

        if percept['food_here']:
            action = 'Up'
        elif unvisited_moves:
            # Move to the first unvisited non-wall cell
            action = unvisited_moves[0]
        else:
            # If all neighboring cells are visited/walls, choose a different action to break out
            action = 'Right' if self.last_action in ['Up', 'Left'] else 'Left'

        self.last_action = action
        return action


# Lab 02 
from collections import deque

class SearchAgent:

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        width, height = grid_size
        queue = deque([(start_pos, [])])
        visited = {start_pos}

        while queue:
            curr_pos, path = queue.popleft()
            if curr_pos == goal_pos:
                return path

            cx, cy = curr_pos
            for direction, (dx, dy) in [('Up', (0, 1)), ('Down', (0, -1)), ('Left', (-1, 0)), ('Right', (1, 0))]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    next_pos = (nx, ny)
                    if next_pos not in walls and next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, path + [direction]))
        return None

