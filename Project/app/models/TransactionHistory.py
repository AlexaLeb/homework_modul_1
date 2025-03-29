# from .Transaction import Transaction
#
#
# class TransactionHistory:
#     def __init__(self):
#         self.transactions = []  # Список объектов Transaction
#
#     def add_transaction(self, transaction: Transaction):
#         self.transactions.append(transaction)
#
#     def get_all(self):
#         return self.transactions

# app/models/prediction_history.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlmodel import SQLModel
from . import Base

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class PredictionHistory(SQLModel, table=True):
    __tablename__ = "prediction_histories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    details: Optional[str] = Field(default=None, nullable=True)  # Детали предсказания (например, JSON)
    timestamp: datetime = Field(default_factory=datetime.utcnow)



