# test_env.py
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

try:
    import gymnasium as gym
except ImportError:
    import gym  # type: ignore

import parking_env  # يسجّل البيئة Parking-v0

RENDER_MODE = "no_render"   # "human" أو "rgb_array"
OBS_TYPE    = "vector"      # "rgb" أو "vector"
ACTION_TYPE = "discrete"    # غيّرها لما يطبع عندك من القائمة المسموحة

env = gym.make(
    "Parking-v0",
    render_mode=RENDER_MODE,
    observation_type=OBS_TYPE,
    action_type=ACTION_TYPE,
)

reset_out = env.reset()
obs = reset_out[0] if isinstance(reset_out, tuple) else reset_out

total = 0.0
for _ in range(50):
    action = env.action_space.sample()
    step_out = env.step(action)
    if len(step_out) == 5:  # Gymnasium
        obs, reward, terminated, truncated, info = step_out
        done = terminated or truncated
    else:                   # Gym 0.26
        obs, reward, done, info = step_out
    total += float(reward)
    if done:
        reset_out = env.reset()
        obs = reset_out[0] if isinstance(reset_out, tuple) else reset_out

env.close()
print("[OK] total reward:", total)