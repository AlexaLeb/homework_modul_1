import bcrypt
from .TransactionHistory import TransactionHistory
from .PredictionHistory import PredictionHistory


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
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Один к одному с балансом
    balance = relationship("Balance", back_populates="user", uselist=False)
    # Один ко многим с транзакциями
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        import bcrypt
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    # --- Методы для работы с БД ---
    @classmethod
    def create(cls, session, username: str, password: str, is_admin: bool = False):
        user = cls(username=username, hashed_password="")
        user.set_password(password)
        user.is_admin = is_admin
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_username(cls, session, username: str):
        return session.query(cls).filter_by(username=username).first()

