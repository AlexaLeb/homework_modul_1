from models.Prediction_task import PredictionTask
from logger.logging import get_logger

logger = get_logger(logger_name=__name__)


def create(session, user_id: int, budget_amount: float, preferences: str, fake=None):
    task = PredictionTask(user_id=user_id, budget_amount=budget_amount, preferences=preferences)
    session.add(task)
    session.commit()
    logger.info('Создано задание на предсказание')

    if fake:
        return task, fake
    return task


def get_all(session):
    return session.query(PredictionTask).all()


def get_by_user_id(session, user_id: int):
    return session.query(PredictionTask).filter_by(user_id=user_id).all()


