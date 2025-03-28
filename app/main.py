from models.Balance import Balance
from models.Transaction import Transaction
from models.PredictionTask import PredictionTask
from models.MLModel import MLModel
from models.BudgetRecommendationModel import BudgetRecommendationModel
from models.AlternativeBudgetModel import AlternativeBudgetModel
from models.TransactionHistory import TransactionHistory
from models.User import User
from models.AdminUser import AdminUser


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
    task = PredictionTask(1, user.user_id, 50000, preferences, user.transaction_history, user.prediction_history)

    modelB = BudgetRecommendationModel('modelA')
    modelA = AlternativeBudgetModel('modelB')

    for model in [modelB, modelA]:
        task.run(model)
        # Вывод результата, если задача выполнена успешно
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