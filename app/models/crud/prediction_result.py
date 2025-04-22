from models.Prediction_result import PredictionResult
from logger.logging import get_logger

logger = get_logger(logger_name=__name__)


def create(session, task_id: int, recommended_distribution: str):
    result = PredictionResult(task_id=task_id, recommended_distribution=recommended_distribution)
    session.add(result)
    session.commit()
    logger.info("Создан результат предсказания")
    return result


def get_all(session):
    return session.query(PredictionResult).all()


def get_by_task_id(session, task_id: int):
    return session.query(PredictionResult).filter_by(task_id=task_id).first()
