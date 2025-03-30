


# class User:
#     def __init__(self, user_id: int, username: str, password: str):
#         self.user_id = user_id                  # Идентификатор пользователя
#         self.username = username                # Имя пользователя
#         self.hashed_password = self.hash_password(password)  # Хэшированный пароль
#         self.transaction_history = TransactionHistory()  # Отдельная сущность для истории транзакций
#         self.prediction_history = PredictionHistory()    # Отдельная сущность для истории предсказаний
#         self.is_admin = False
#
#         # Приватный метод для хэширования пароля
#     def hash_password(self, password: str) -> bytes:
#         return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#
#         # Метод для проверки пароля
#     def check_password(self, password: str) -> bool:
#         return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)
#
#         # Метод для смены пароля
#     def set_password(self, new_password: str):
#         self.hashed_password = self.hash_password(new_password)

# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel
from . import Base
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'

    # Определяем поле id с типом Optional[int] и указываем, что оно является первичным ключом.
    id: Optional[int] = Field(default=None, primary_key=True)

    # Поле username с указанием дополнительных параметров через sa_column
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})

    # Поле hashed_password, обязательное для заполнения
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})

    # Флаг администратора, по умолчанию False
    is_admin: bool = Field(default=False, sa_column_kwargs={"default": False})

    # Определяем связь "один к одному" с балансом
    balance: Optional["Balance"] = Relationship(back_populates="user")

    # Определяем связь "один ко многим" с транзакциями, используем тип List для множественных записей
    transactions: List["Transaction"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Новая связь "один ко многим" с задачами предсказаний
    prediction_tasks: List["PredictionTask"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def set_password(self, password: str):
        import bcrypt
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
