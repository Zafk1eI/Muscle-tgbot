from db import models
import random


async def get_random_record():
    record = await models.Muscle.all().count()
    random_id = random.randint(1, record)
    muscle = await models.Muscle.filter(id=random_id).first()
    return muscle


async def user_has_seen_all_records(user_id: int) -> bool:
    all_muscles = await models.Muscle.all()
    all_muscle_ids = [muscle.id for muscle in all_muscles]
    user_answered_muscle_ids = await models.UsersMuscles.filter(user_id=user_id).values_list('muscle_id_id', flat=True)
    for muscle_id in all_muscle_ids:
        if muscle_id not in user_answered_muscle_ids:
            return True
    return False


async def get_top_10_users() -> list:
    return await models.User.filter().order_by("answer_count").limit(10).all()

