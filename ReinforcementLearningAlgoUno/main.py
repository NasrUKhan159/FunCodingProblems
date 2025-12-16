# Problem: Build a reinforcement learning algorithm without using high-level Python packages e.g. RLCard
# to model strategies by players in an Uno game. This runner uses the simple opponent for Player 1 and the (currently
# naive) RL agent placeholder for Player 0.
# Downside of solution: missing opponent logic (the opponent has no code to take a turn, so the game loop will
# break immediately. Secondly, the QLearningAgent uses str(state) as a key, which quickly becomes unwieldy and
# inefficient in complex game states. Thirdly, the actions need careful definition (e.g. distinguishing b/w playing
# index 3 and the string 'draw'). For these reasons, RLCard builds a more robust RL environment for modelling card games

import time
from uno_core import UnoEnvironment, QLearningAgent, simple_opponent_play

def run_training(num_episodes = 100):
    agent = QLearningAgent()

    print(f"Starting simulation for {num_episodes} episodes...")
    win_count_agent = 0
    start_time = time.time()

    for episode in range(num_episodes):
        env = UnoEnvironment(num_players=2)
        done = False

        while not done:
            player_id = env.current_player
            call_color = None

            if player_id == 0:
                legal_actions = env.get_legal_actions(player_id)
                # Uising simple_opponent_play for now since RL agent is a stub
                action, call_color = simple_opponent_play(env, player_id)

                next_state, reward, done = env.step(player_id, action, call_color)
                # agent.learn(state, action, reward, next_state) # RL update call

            else:
                action, call_color = simple_opponent_play(env, player_id)
                env.step(player_id, action, call_color)

            if done:
                if len(env.players[0])==0:
                    win_count_agent += 1
                break

        if episode % 10 == 0:
            print(f"Episode {episode} finished.")

    end_time = time.time()
    print(f"\nSimulation finished in {end_time - start_time:.2f} seconds.")
    print(f"Agent Win Rate: {win_count_agent / num_episodes * 100:.2f}%")

if __name__ == "__main__":
    run_training(num_episodes=70)