import datetime


class PredictionResult:
    def __init__(self, task_id: int, recommended_distribution: dict):
        self.task_id = task_id
        self.recommended_distribution = recommended_distribution
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
