# from .PredictionTask import PredictionTask
#
#
# # Класс PredictionHistory для хранения истории выполненных задач предсказания
# class PredictionHistory:
#     def __init__(self):
#         self.predictions = []  # Список объектов PredictionTask
#
#     def add_prediction(self, prediction_task: PredictionTask):
#         self.predictions.append(prediction_task)
#
#     def get_all(self):
#         return self.predictions


# app/models/prediction_history.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class PredictionHistory(SQLModel, table=True):
    __tablename__ = "prediction_histories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    details: Optional[str] = Field(default=None, nullable=True)  # Детали предсказания (например, JSON)
    timestamp: datetime = Field(default_factory=datetime.now)

