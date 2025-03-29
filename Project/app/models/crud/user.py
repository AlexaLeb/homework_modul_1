from ..User import User


def create_user(session, username: str, password: str, is_admin: bool = False):
    user = User(username=username, hashed_password="")
    user.set_password(password)
    user.is_admin = is_admin
    session.add(user)
    session.commit()
    return user


def get_all_users(session):
    return session.query(User).all()


def get_by_username(session, username: str):
    return session.query(User).filter_by(username=username).first()