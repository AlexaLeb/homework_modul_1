from .Transaction import Transaction


class TransactionHistory:
    def __init__(self):
        self.transactions = []  # Список объектов Transaction

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_all(self):
        return self.transactions
