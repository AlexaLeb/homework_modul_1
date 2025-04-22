from sqlmodel import SQLModel


class MLModel(SQLModel, table=True):
    __abstract__ = True  # Этот класс не будет отображаться в виде таблицы
