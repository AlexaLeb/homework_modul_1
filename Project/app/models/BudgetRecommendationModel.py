from .MLModel import MLModel


# Класс BudgetRecommendationModel наследуется от MLModel и реализует метод predict
class BudgetRecommendationModel(MLModel):
    def predict(self, data, budget_amount: float, preferences: dict) -> dict:
        """
        data: история транзакций пользователя
        budget_amount: общий бюджет
        preferences: словарь приоритетов для категорий
        """
        # Для простоты предположим, что тип транзакции может быть использован как категория
        # Отбираем транзакции, отличные от обычных пополнений и списаний
        # Взаимодействие с моделью
        # Для проверки работоспособности я написал небольшой код, чтобы можно было изменения в данных увидеть
        total_weight = sum(preferences.values())
        recommended = {}
        for category, weight in preferences.items():
            recommended[category] = (weight / total_weight) * budget_amount
        return recommended
# app/models/budget_recommendation_model.py
# from .MLModel import MLModel
# from sqlalchemy import Column, Integer, Float, String
#
#
#
# class BudgetRecommendationModel(MLModel):
#     __tablename__ = 'budget_recommendation_models'
#
#     id = Column(Integer, primary_key=True)
#     amount = Column(String, nullable=False)
#
#
#
#     def predict(self, data, budget_amount: float, preferences: dict) -> dict:
#         total_weight = sum(preferences.values())
#         recommended = {}
#         for category, weight in preferences.items():
#             recommended[category] = (weight / total_weight) * budget_amount
#         return recommended
#
#     # --- Методы для работы с БД ---
#     @classmethod
#     def create(cls, session, model_name: str):
#         instance = cls()  # Здесь можно сохранить model_name, если добавить соответствующее поле
#         session.add(instance)
#         session.commit()
#         return instance
#
#     @classmethod
#     def get_all(cls, session):
#         return session.query(cls).all()
