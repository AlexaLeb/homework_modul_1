import bcrypt
from .TransactionHistory import TransactionHistory
from .PredictionHistory import PredictionHistory


class User:
    def __init__(self, user_id: int, username: str, password: str):
        self.user_id = user_id                  # Идентификатор пользователя
        self.username = username                # Имя пользователя
        self.hashed_password = self.hash_password(password)  # Хэшированный пароль
        self.transaction_history = TransactionHistory()  # Отдельная сущность для истории транзакций
        self.prediction_history = PredictionHistory()    # Отдельная сущность для истории предсказаний
        self.is_admin = False

        # Приватный метод для хэширования пароля
    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Метод для проверки пароля
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)

        # Метод для смены пароля
    def set_password(self, new_password: str):
        self.hashed_password = self.hash_password(new_password)
