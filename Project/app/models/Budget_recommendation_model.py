from MLModel import MLModel


class BudgetRecommendationModel(MLModel):
    __abstract__ = True

    def predict(self, data, budget_amount: float, preferences: dict) -> dict:
        total_weight = sum(preferences.values())
        recommended = {}
        for category, weight in preferences.items():
            recommended[category] = (weight / total_weight) * budget_amount
        return recommended
