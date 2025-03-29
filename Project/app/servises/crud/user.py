from


def create(cls, session, username: str, password: str, is_admin: bool = False):
    user = cls(username=username, hashed_password="")
    user.set_password(password)
    user.is_admin = is_admin
    session.add(user)
    session.commit()
    return user


@classmethod
def get_all(cls, session):
    return session.query(cls).all()


@classmethod
def get_by_username(cls, session, username: str):
    return session.query(cls).filter_by(username=username).first()