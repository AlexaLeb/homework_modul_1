# class Balance:
#     def __init__(self, user_id: int, amount: float = 0.0):
#         self.user_id = user_id
#         self._amount = amount
#
#     # Метод для пополнения баланса
#     def deposit(self, amount: float):
#         self._amount += amount
#
#     # Метод для списания баланса
#     def withdraw(self, amount: float):
#         if self._amount >= amount:
#             self._amount -= amount
#         else:
#             raise Exception("Недостаточно средств")
#
#     def get_amount(self) -> float:
#         return self._amount

# app/models/balance.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Balance(SQLModel, table=True):
    __tablename__ = "balances"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    amount: float = Field(default=0.0)

    # Определяем связь с моделью User (один к одному)
    user: Optional["User"] = Relationship(back_populates="balance")

    def deposit(self, amount: float):
        self.amount += amount
        print(self.amount)

    def withdraw(self, amount: float):
        if self.amount >= amount:
            self.amount -= amount
            print(self.amount)
        else:
            raise Exception("Недостаточно средств для списания")

    def get_amount(self) -> float:
        return self.amount

