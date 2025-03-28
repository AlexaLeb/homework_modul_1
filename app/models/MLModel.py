class MLModel:
    def __init__(self, name):
        self.name = name  # Имя модели

        def predict(self, data, budget_amount: float, preferences: dict) -> dict:
            raise NotImplementedError("Метод predict должен быть реализован в наследниках")
