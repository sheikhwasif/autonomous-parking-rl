import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # احذفها لو بتعرض نافذة

try:
    import gymnasium as gym
except ImportError:
    import gym  # type: ignore

import parking_env  # يسجل env: "Parking-v0"
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

ENV_KW = dict(render_mode="no_render", observation_type="vector", action_type="discrete")

env = gym.make("Parking-v0", **ENV_KW)
env = Monitor(env)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./tb_logs")
model.learn(total_timesteps=20_000)  # كبّر الرقم لاحقاً
model.save("ppo_parking_vec_discrete")
env.close()
print("[TRAIN DONE]")