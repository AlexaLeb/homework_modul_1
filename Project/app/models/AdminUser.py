from .User import User


class AdminUser(User):
    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password)
        self.is_admin = True

    # Администратор может пополнять баланс любого пользователя
    def modify_balance(self, balance_obj, amount: float):
        balance_obj.deposit(amount)