# utils/env.py

import gym
import numpy as np

class TradingEnv(gym.Env):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.current_step = 0
        self.prices = np.random.rand(100)  # substitua por dados reais
        self.action_space = gym.spaces.Discrete(3)  # 0 = hold, 1 = buy, 2 = sell
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return np.array([self.prices[self.current_step]])

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= len(self.prices) - 1
        reward = np.random.randn()  # simulado
        obs = np.array([self.prices[self.current_step]])
        return obs, reward, done, {}
