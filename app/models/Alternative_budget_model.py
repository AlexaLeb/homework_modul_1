from .MLModel import MLModel


class AlternativeBudgetModel(MLModel):
    def predict(self, data, budget_amount: float, preferences: dict) -> dict:
        num_categories = len(preferences)
        if num_categories == 0:
            return {}
        equal_share = budget_amount / num_categories
        recommended = {category: equal_share for category in preferences.keys()}
        return recommended
