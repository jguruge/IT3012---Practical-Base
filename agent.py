# agent.py
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




















