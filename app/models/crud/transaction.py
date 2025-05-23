from models.Transaction import Transaction
from logger.logging import get_logger

logger = get_logger(logger_name=__name__)


def create(session, user_id: int, transaction_type: str, amount: float):
    transaction = Transaction(user_id=user_id, transaction_type=transaction_type, amount=amount)
    session.add(transaction)
    session.commit()
    logger.info("Создана транзакция")
    return transaction


def get_all(session):
    return session.query(Transaction).all()


def get_by_user_id(session, user_id: int):
    return session.query(Transaction).filter_by(user_id=user_id).all()


def get_by_type(session, transaction_type: str):
    return session.query(Transaction).filter_by(transaction_type=transaction_type).all()
