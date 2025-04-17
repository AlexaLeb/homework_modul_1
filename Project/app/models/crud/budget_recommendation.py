from models.Budget_recommendation_model import BudgetRecommendationModel


def create(cls, session, model_name: str):
    instance = cls()  # Здесь можно сохранить model_name, если добавить соответствующее поле
    session.add(instance)
    session.commit()
    return instance


def get_all(cls, session):
    return session.query(cls).all()