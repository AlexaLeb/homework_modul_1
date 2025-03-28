class Transaction:
    def __init__(self, user_id: int, transaction_type: str, amount: float):
        self.user_id = user_id                     # Пользователь, к которому относится транзакция
        self.transaction_type = transaction_type  # Тип транзакции
        self.amount = amount                  # Сумма транзакции
