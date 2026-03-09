# record_video.py
import os, time
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # تشغيل بدون نافذة

# جرّب gymnasium أولاً وإلا استخدم gym
try:
    import gymnasium as gym
except ImportError:
    import gym  # type: ignore

import imageio.v2 as imageio
import numpy as np
import parking_env  # مهم للتسجيل مع gym
from stable_baselines3 import PPO

# إعداد البيئة والنموذج
env = gym.make(
    "Parking-v0",
    render_mode="rgb_array",
    observation_type="vector",
    action_type="discrete"
)

model_path = "models/ppo_parking.zip"
model = PPO.load(model_path)

# فيديو آوت
os.makedirs("videos", exist_ok=True)
mp4_path = "videos/parking_demo.mp4"
gif_path = "videos/parking_demo.gif"

# FPS من الميتاداتا إن وُجد وإلا 30
fps = getattr(getattr(env, "metadata", {}), "get", lambda *_: None)("render_fps") or \
      (env.metadata["render_fps"] if isinstance(getattr(env, "metadata", None), dict) and "render_fps" in env.metadata else 30)

duration_steps = 800  # عدد الخطوات القصوى (يمكن تغييره)
frames = 0

# كاتب MP4 بالستريم (أفضل أداء من تخزين كل الإطارات في الذاكرة)
mp4_writer = imageio.get_writer(mp4_path, fps=fps, codec="libx264", quality=8)

# حلقة توليد الفيديو
reset_out = env.reset()
obs = reset_out[0] if isinstance(reset_out, tuple) else reset_out

while frames < duration_steps:
    # توقّع أكشن
    action, _ = model.predict(obs, deterministic=True)

    # خطوة
    step_out = env.step(action)
    if len(step_out) == 5:
        obs, reward, terminated, truncated, info = step_out
        done = terminated or truncated
    else:
        obs, reward, done, info = step_out

    # اطلب فريم RGB وأضفه للكاتب
    frame = env.render()
    if frame is not None:
        mp4_writer.append_data(frame)
        frames += 1

    if done:
        # أعِد الضبط وكمّل الفيديو من حلقة جديدة
        reset_out = env.reset()
        obs = reset_out[0] if isinstance(reset_out, tuple) else reset_out

mp4_writer.close()
env.close()
print(f"[SAVED] {mp4_path}")

# تحويل نسخة GIF سريعة (اختياري)
# ملاحظة: نعيد قراءة mp4 للإخراج كـ GIF لتفادي حفظ كل الإطارات في الذاكرة.
try:
    reader = imageio.get_reader(mp4_path)
    gif_writer = imageio.get_writer(gif_path, fps=min(fps, 15))  # GIF أصغر
    for im in reader:
        gif_writer.append_data(im)
    gif_writer.close()
    reader.close()
    print(f"[SAVED] {gif_path}")
except Exception as e:
    print("[WARN] GIF convert failed:", e)