from .PredictionTask import PredictionTask


# Класс PredictionHistory для хранения истории выполненных задач предсказания
class PredictionHistory:
    def __init__(self):
        self.predictions = []  # Список объектов PredictionTask

    def add_prediction(self, prediction_task: PredictionTask):
        self.predictions.append(prediction_task)

    def get_all(self):
        return self.predictions
