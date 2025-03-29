# class MLModel:
#     def __init__(self, name):
#         self.name = name  # Имя модели
#
#         def predict(self, data, budget_amount: float, preferences: dict) -> dict:
#             raise NotImplementedError("Метод predict должен быть реализован в наследниках")

# app/models/ml_model.py
from . import Base
from sqlmodel import SQLModel


class MLModel(SQLModel,table=True):
    __abstract__ = True  # Этот класс не будет отображаться в виде таблицы

