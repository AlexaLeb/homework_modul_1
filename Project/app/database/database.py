from sqlmodel import SQLModel, Session, create_engine

from .config import get_settings
from models.crud import balance, mlmodel, predicitonHistory, predictionresult, predictiontask, transaction, user


# Создаем движок на основе URL, полученного из настроек
engine = create_engine(
    url=get_settings().DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)


# Функция-генератор для получения сессии. Используем with-контекст, чтобы автоматически закрыть сессию.
def get_session():
    with Session(engine) as session:
        yield session


# Инициализация базы данных: дропаем существующие таблицы и создаём заново
def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        alex = user.create_user(session, 'Alex', '11', False)
        user.create_user(session, 'Nasta', '12', False)
        user.create_user(session, 'Admin', '13', True)

        dmb = balance.create(session, user_id=alex.id, initial_amount=1000)
        balance.create(session, user_id=user.get_by_username(session, 'Nasta').id, initial_amount=800)
        alex.balance = dmb

        transaction.create(session, user_id=alex.id, transaction_type='deposit', amount=200)
        transaction.create(session, user_id=user.get_by_username(session, 'Nasta').id, transaction_type='withdraw', amount=100)

        session.commit()
        session.close()
        print('BD susseced updated')



