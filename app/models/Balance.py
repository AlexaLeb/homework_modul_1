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

    def get_amount(self) -> float:
        return self._amount
