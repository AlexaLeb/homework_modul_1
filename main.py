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


class AdminUser(User):
    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password)
        self.is_admin = True

    # Администратор может пополнять баланс любого пользователя
    def modify_balance(self, balance_obj, amount: float):
        balance_obj.deposit(amount)


# Класс транзакции для истории операций
class Transaction:
    def __init__(self, user: User, transaction_type: str, amount: float):
        self.user = user                      # Пользователь, к которому относится транзакция
        self.transaction_type = transaction_type  # Тип транзакции
        self.amount = amount                  # Сумма транзакции


# Класс TransactionHistory для хранения истории транзакций пользователя
class TransactionHistory:
    def __init__(self):
        self.transactions = []  # Список объектов Transaction

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_all(self):
        return self.transactions


class Balance:
    def __init__(self, user_id: int, amount: float = 0.0):
        self.user_id = user_id
        self._amount = amount

    # Метод для пополнения баланса
    def deposit(self, amount: float):
        self._amount += amount

    # Метод для списания баланса
    def withdraw(self, amount: float):
        if self._amount >= amount:
            self._amount -= amount
        else:
            raise Exception("Недостаточно средств")

    # Метод для получения текущего баланса
    def get_amount(self) -> float:
        return self._amount


# Базовый класс ML модели
class MLModel:
    def __init__(self, name):
        self.name = name  # Имя модели

        def predict(self, data, budget_amount: float, preferences: dict) -> dict:
            raise NotImplementedError("Метод predict должен быть реализован в наследниках")


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
        # Взаимодействие с моделью, для примера просто какие-то цифры считаю
        total_weight = sum(preferences.values())
        recommended = {}
        for category, weight in preferences.items():
            recommended[category] = (weight / total_weight) * budget_amount
        return recommended


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

# Альтернативная модель для демонстрации полиморфизма: реализует predict другим способом.
class AlternativeBudgetModel(MLModel):
    def predict(self, data, budget_amount: float, preferences: dict) -> dict:
        num_categories = len(preferences)
        if num_categories == 0:
            return {}
        equal_share = budget_amount / num_categories
        recommended = {category: equal_share for category in preferences.keys()}
        return recommended



if __name__ == "__main__":
    # Создаем обычного пользователя с хэшированным паролем
    user = User(1, "ivan", "password123")
    # Создаем баланс для пользователя (баланс хранится отдельно)
    user_balance = Balance(user.user_id, 100.0)

    # Создаем администратора
    admin = AdminUser(2, "admin", "adminpass")

    # Добавляем транзакции в историю пользователя
    user.transaction_history.add_transaction(Transaction(user.user_id, "Food", 1500))
    user.transaction_history.add_transaction(Transaction(user.user_id, "Transport", 500))
    user.transaction_history.add_transaction(Transaction(user.user_id, "Entertainment", 800))

    # Создаем задачу предсказания с приоритетами для категорий
    preferences = {"Food": 2, "Transport": 1, "Entertainment": 1}
    task = PredictionTask(1, user, 50000, preferences)

    # Это полиморфизм?
    modelB = BudgetRecommendationModel('modelA')
    modelA = AlternativeBudgetModel('modelB')

    for model in [modelB, modelA]:
        task.run(model)
        result = task.get_result()
        if result:
            print("\nРекомендованное распределение бюджета:")
            for category, amount in result.recommended_distribution.items():
                print(f"{category}: {amount:.2f}")
        else:
            print("Ошибка выполнения задачи:", task.validation_errors)

    # Демонстрация проверки пароля
    print("\nПроверка пароля для пользователя ivan (правильный):", user.check_password("password123"))
    print("\nПроверка пароля для пользователя ivan (неправильный):", user.check_password("hfvdjd"))

    # Демонстрация работы администратора: пополнение баланса пользователя
    try:
        admin.modify_balance(user_balance, 50)
        print("\nНовый баланс пользователя:", user_balance.get_amount())
    except Exception as e:
        print("Ошибка пополнения баланса:", e)