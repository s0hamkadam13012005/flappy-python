import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

env = gym.make('CartPole-v1', render_mode="human")
total_rewards = []
episodes = 10

for episode in range(episodes):
    state, _ = env.reset()
    episode_reward = 0
    for step in range(200):
        env.render()
        action = env.action_space.sample()  # random action
        next_state, reward, terminated, truncated, _ = env.step(action)
        episode_reward += reward
        if terminated or truncated:
            break
    total_rewards.append(episode_reward)
    print(f"Episode {episode + 1}: Total reward = {episode_reward}")

env.close()

plt.figure(figsize=(8, 5))
plt.plot(range(1, episodes + 1), total_rewards, marker='o')
plt.xlabel("Episode")
plt.ylabel("Total rewards")
plt.title("Random Agent on CartPole")
plt.grid(True)
plt.tight_layout()
plt.show()


