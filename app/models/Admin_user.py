from .User import User


class AdminUser(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin = True
