"""
Описание идеи:
Сервис для определения оптимального распределения расходов (бюджетирование)
Суть: Пользователь вводит свой текущий бюджет и планируемые траты, а модель рекомендует, как лучше распределить средства
(например, на основе правил «не трать больше 30% на развлечения», «не более 40% на кредиты» и т.д.).

"""

import bcrypt
import datetime


# Класс пользователя
class User:
    def __init__(self, user_id: int, username: str, password: str, balance: float):
        self.user_id = user_id            # Идентификатор пользователя
        self.username = username          # Имя пользователя
        self.password = password          # Пароль
        self.balance = balance            # Баланс
        self.transaction_history = []     # Список транзакций
        self.prediction_tasks = []        # Список задач предсказания

        # Приватный метод для хэширования пароля
    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Метод для проверки пароля
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)

        # Метод для смены пароля
    def set_password(self, new_password: str):
        self.hashed_password = self.hash_password(new_password)


# Класс транзакции для истории операций
class Transaction:
    def __init__(self, user: User, transaction_type: str, amount: float):
        self.user = user                      # Пользователь, к которому относится транзакция
        self.transaction_type = transaction_type  # Тип транзакции
        self.amount = amount                  # Сумма транзакции


# Базовый класс ML модели
class MLModel:
    def __init__(self, name):
        self.name = name  # Имя модели


# Класс BudgetRecommendationModel наследуется от MLModel и реализует метод predict
class BudgetRecommendationModel(MLModel):
    def predict(self, data, budget_amount: float, preferences: dict) -> dict:
        """
        data: история транзакций пользователя
        budget_amount: общий бюджет
        preferences: словарь приоритетов для категорий
        """
        # Для простоты предположим, что тип транзакции может быть использован как категория
        # Отбираем транзакции, отличные от обычных пополнений и списаний
        # Взаимодействие с моделью
        return "Результат взаимодействия"


# Класс задачи предсказания
class PredictionTask:
    def __init__(self, task_id: int, user: User, budget_amount: float, preferences: dict):
        self.task_id = task_id                # Уникальный идентификатор задачи
        self.user = user                      # Пользователь, создавший задачу
        self.budget_amount = budget_amount    # Введённый бюджет
        self.preferences = preferences        # Приоритеты категорий (словарь)
        self.status = "NEW"                   # Статус задачи: NEW, PROCESSING, COMPLETED, ERROR
        self.result = None                    # Результат предсказания (объект PredictionResult)
        self.validation_errors = []           # Список ошибок валидации (если есть)

    def run(self, model: MLModel):  # Создание предсказания
        self.status = "PROCESSING"
        if self.budget_amount <= 0:
            self.status = "ERROR"
            self.validation_errors.append("Бюджет должен быть больше нуля")
            return
        if not self.user.transaction_history:
            self.status = "ERROR"
            self.validation_errors.append("Отсутствует история транзакций пользователя")
            return

        recommended_distribution = model.predict(
            self.user.transaction_history.get_all(),
            self.budget_amount,
            self.preferences
        )
        self.result = PredictionResult(self.task_id, recommended_distribution)
        self.status = "COMPLETED"
        # Добавляем задачу в историю предсказаний пользователя
        self.user.prediction_history.add_prediction(self)
        # Добавляем транзакцию за списание условных кредитов (например, -5)
        fee_transaction = Transaction(self.user.user_id, "prediction_fee", -5)
        self.user.transaction_history.add_transaction(fee_transaction)

    # Метод для получения результата задачи
    def get_result(self):
        return self.result


class PredictionResult:
    def __init__(self, task_id: int, recommended_distribution: dict):
        self.task_id = task_id
        self.recommended_distribution = recommended_distribution
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Класс PredictionHistory для хранения истории выполненных задач предсказания
class PredictionHistory:
    def __init__(self):
        self.predictions = []  # Список объектов PredictionTask

    def add_prediction(self, prediction_task: PredictionTask):
        self.predictions.append(prediction_task)

    def get_all(self):
        return self.predictions


# Пример использования объектной модели
if __name__ == "__main__":
    pass
