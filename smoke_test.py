# --- Minimal smoke test for parking-env ---

# أولوية: نحاول استخدام gym (المكتبة التي ثبّتناها)،
# ولو ما اشتغل تعريف البيئة بالـID، نجرب استيراد الكلاس مباشرة.

import sys

# جرّب gym أولاً
try:
    import gym
    G = gym
except Exception:
    # احتياط: لو ما كان gym متاح نحاول gymnasium (مو لازم هنا، لكن كخطة ب)
    import gymnasium as gym
    G = gym

# قائمة احتمالات لأسماء البيئة (لأن بعض الريبوز تسميها بشكل مختلف)
CANDIDATE_IDS = [
    "parking-v0",
    "Parking-v0",
    "SelfParking-v0",
    "self-parking-v0",
]

env = None
last_err = None

# جرّب إنشاء البيئة بالـID
for env_id in CANDIDATE_IDS:
    try:
        env = G.make(env_id)  # بدون render_mode عشان نتجنب فتح نافذة
        print(f"[OK] Made env by id: {env_id}")
        break
    except Exception as e:
        last_err = e

# لو ما زبطت الـID، جرّب استيراد الكلاس مباشرة
if env is None:
    try:
        # أكثر اسم متوقع للموديول/الباكيج داخل الريبو
        # عدّل المسار إذا كان اسم المجلد مختلف داخل المشروع
        from parking_env.envs.parking_env import ParkingEnv  # احتمال شائع
    except Exception:
        try:
            from parking_env import ParkingEnv  # احتمال آخر
        except Exception as e2:
            print("[ERR] Couldn't import ParkingEnv class.")
            print("Last gym.make error:", repr(last_err))
            print("Import error:", repr(e2))
            sys.exit(1)
    # أنشئ البيئة من الكلاس مباشرة
    env = ParkingEnv()
    print("[OK] Made env from ParkingEnv class")

# لفّة خطوات بسيطة
obs = env.reset()
print("reset() -> obs shape/type:", type(obs), getattr(obs, "shape", None))

total_reward = 0.0
for step in range(100):
    # فعل عشوائي
    try:
        action = env.action_space.sample()
    except Exception:
        action = 0  # في حال الأكشن سبايس غير معرّف، اختيار افتراضي
    out = env.step(action)

    # دعم كلا من gym و gymnasium في قيم step
    if len(out) == 5:
        obs, reward, terminated, truncated, info = out
        done = terminated or truncated
    else:
        obs, reward, done, info = out

    total_reward += float(reward)
    if done:
        print(f"Episode done at step {step}")
        break

print("Total reward:", total_reward)
env.close()
print("[SMOKE TEST PASSED]")
