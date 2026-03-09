# parking_env/__init__.py
# نسجل البيئة عند الاستيراد
try:
    # إذا كنت ستستخدم Gymnasium لاحقًا داخل الأكواد الأخرى، لا بأس أن يظل التسجيل من Gymnasium
    from gymnasium.envs.registration import register
except ImportError:
    # احتياط لو بيئة العمل فيها Gym فقط
    from gym.envs.registration import register  # type: ignore

register(
    id="Parking-v0",                     # هذا هو الاسم الذي سنناديه به
    entry_point="parking_env.parking:Parking",
)