from models.Balance import Balance
from models.Transaction import Transaction
from models.PredictionTask import PredictionTask
from models.MLModel import MLModel
from models.BudgetRecommendationModel import BudgetRecommendationModel
from models.AlternativeBudgetModel import AlternativeBudgetModel
from models.TransactionHistory import TransactionHistory
from models.User import User
from models.AdminUser import AdminUser
from database.config import get_settings
from database.database import init_db, get_session
from sqlmodel import Session


if __name__ == "__main__":

    settings = get_settings()
    print(settings.DB_HOST)
    print(settings.DB_NAME)

    init_db()
    print('init db success')