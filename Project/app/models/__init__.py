# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Импорт моделей для их регистрации (порядок может быть важен при наличии зависимостей)
from .User import User
from .AdminUser import AdminUser
from .Balance import Balance
from .Transaction import Transaction
# При необходимости можно импортировать и другие модели:
# from .prediction_task import PredictionTask
# from .prediction_result import PredictionResult
# from .prediction_history import PredictionHistory
