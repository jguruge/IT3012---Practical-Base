from grid_game import GridHuntGame
from agent import ModelBasedAgent#Lab02

def run_grid_hunt():
    env = GridHuntGame()
    agent = ModelBasedAgent()#Lab02

    print("=== Model-Based Agent Simulation Started ===")

    while not env.is_done():
        percept = env.get_percept(agent)
        action = agent.sense_and_act(percept)

        print(f"Wall Ahead: {percept['wall_ahead']}")
        print(f"Food Here: {percept['food_here']}")
        print(f"Action: {action}")

        env.execute_action(agent, action)

        print(f"Score: {env.score} | Steps: {env.steps}")
        print("--------------------")

    print(f"\nGame Over! Final Score: {env.score} after {env.steps} steps.")

if __name__ == "__main__":
    run_grid_hunt()