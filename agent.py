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
        self.visited_cells = set()
        self.known_walls = set()
        self.current_pos = (0, 0)
        self.facing = 'Up'
        self.last_action = None

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

        self.visited_cells.add(self.current_pos)

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
            left_visited = (left_cell in self.visited_cells or left_cell in self.known_walls)
            right_visited = (right_cell in self.visited_cells or right_cell in self.known_walls)
            if left_visited and not right_visited:
                action = 'turn_right'
            else:
                action = 'turn_left'
        else:
            front_visited = (front_cell in self.visited_cells)
            left_visited = (left_cell in self.visited_cells or left_cell in self.known_walls)
            right_visited = (right_cell in self.visited_cells or right_cell in self.known_walls)

            if not front_visited:
                action = 'move_forward'
            elif not left_visited:
                action = 'turn_left'
            elif not right_visited:
                action = 'turn_right'
            else:
                action = 'move_forward'

        self.last_action = action
        return action
