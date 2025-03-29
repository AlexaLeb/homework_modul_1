from ..AdminUser import AdminUser


@classmethod
def create_admin(session, username: str, password: str):
    # Создаем администратора, используя метод create у базового класса,
    # затем устанавливаем флаг is_admin в True
    admin = AdminUser.create(session, username, password, is_admin=True)
    return admin

def get_all_Admins(session):
    return session.query(AdminUser).all()
