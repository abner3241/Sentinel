import os
import joblib
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

class RLAgent:
    """Agente de Reinforcement Learning para decidir entradas e saídas."""
    def __init__(self, symbol: str, model_path: str = None):
        self.symbol = symbol
        self.model = None
        if model_path and os.path.exists(model_path):
            self.model = PPO.load(model_path)

    def predict(self, state: dict) -> str:
        if self.model:
            action, _ = self.model.predict(state)
            return {0: 'hold', 1: 'buy', 2: 'sell'}.get(action, 'hold')
        return 'hold'

    def train(self, episodes: int = 1000, timesteps_per_episode: int = 1000):
        from utils.env import TradingEnv
        env = DummyVecEnv([lambda: TradingEnv(self.symbol)])
        model = PPO("MlpPolicy", env, verbose=1)
        total_timesteps = episodes * timesteps_per_episode
        model.learn(total_timesteps=total_timesteps)
        self.model = model

    def save(self, path: str):
        if self.model:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.model.save(path)
        else:
            raise ValueError("Nenhum modelo para salvar")

    @classmethod
    def load(cls, model_path: str):
        agent = cls(symbol=None)
        agent.model = PPO.load(model_path)
        return agent
