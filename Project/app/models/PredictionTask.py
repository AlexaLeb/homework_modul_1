# from .MLModel import MLModel
# from .PredictionResult import PredictionResult
# from .Transaction import Transaction
#
#
# class PredictionTask:
#     def __init__(self, task_id: int, user_id, budget_amount: float, preferences: dict, transaction_history, prediction_history):
#         self.task_id = task_id                # Уникальный идентификатор задачи
#         self.user_id = user_id                   # Пользователь, создавший задачу
#         self.transaction_history = transaction_history
#         self.prediction_history = prediction_history
#         self.budget_amount = budget_amount    # Введённый бюджет
#         self.preferences = preferences        # Приоритеты категорий (словарь)
#         self.status = "NEW"                   # Статус задачи: NEW, PROCESSING, COMPLETED, ERROR
#         self.result = None                    # Результат предсказания (объект PredictionResult)
#         self.validation_errors = []           # Список ошибок валидации (если есть)
#
#     def run(self, model: MLModel):  # Создание предсказания
#         self.status = "PROCESSING"
#         if self.budget_amount <= 0:
#             self.status = "ERROR"
#             self.validation_errors.append("Бюджет должен быть больше нуля")
#             return
#         if not self.transaction_history:
#             self.status = "ERROR"
#             self.validation_errors.append("Отсутствует история транзакций пользователя")
#             return
#
#         recommended_distribution = model.predict(
#             self.transaction_history.get_all(),
#             self.budget_amount,
#             self.preferences
#         )
#         self.result = PredictionResult(self.task_id, recommended_distribution)
#         self.status = "COMPLETED"
#         # Добавляем задачу в историю предсказаний пользователя
#         self.prediction_history.add_prediction(self)
#         # Добавляем транзакцию за списание условных кредитов (например, -5)
#         fee_transaction = Transaction(self.user_id, "prediction_fee", -5)
#         self.transaction_history.add_transaction(fee_transaction)
#
#     # Метод для получения результата задачи
#     def get_result(self):
#         return self.result

# app/models/prediction_task.py
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class PredictionTask(SQLModel, table=True):
    __tablename__ = "prediction_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    budget_amount: float = Field(..., nullable=False)
    preferences: str = Field(..., nullable=False)  # Можно хранить JSON или строковое представление
    status: str = Field(default="NEW")  # Возможные значения: NEW, PROCESSING, COMPLETED, ERROR
    timestamp: datetime = Field(default_factory=datetime.now)

    # Связь с результатом (один к одному)
    result: Optional["PredictionResult"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"uselist": False}
    )

    # Явно указываем условие соединения через primaryjoin
    user: Optional["User"] = Relationship(
        back_populates="prediction_tasks",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == foreign(PredictionTask.user_id)"
        }
    )
