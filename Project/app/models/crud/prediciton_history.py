from models.Prediction_history import PredictionHistory


def create(session, user_id: int, details: str):
    history = PredictionHistory(user_id=user_id, details=details)
    session.add(history)
    session.commit()
    return history


def get_all(session):
    return session.query(PredictionHistory).all()


def get_by_user_id(session, user_id: int):
    return session.query(PredictionHistory).filter_by(user_id=user_id).all()