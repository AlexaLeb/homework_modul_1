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
