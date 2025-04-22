from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class PredictionTask(SQLModel, table=True):
    __tablename__ = "prediction_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    budget_amount: float = Field(..., nullable=False)
    preferences: str = Field(..., nullable=False)  # Можно хранить JSON или строковое представление
    # status: str = Field(default="NEW")  # Возможные значения: NEW, PROCESSING, COMPLETED, ERROR
    timestamp: datetime = Field(default_factory=datetime.now)

    # Связь с результатом (один к одному)
    result: Optional["PredictionResult"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"uselist": False}
    )

    # Явно указываем условие соединения через primaryjoin
    user: Optional["User"] = Relationship(
        back_populates="prediction_tasks",
        sa_relationship_kwargs={
            "primaryjoin": "User.id == foreign(PredictionTask.user_id)"
        }
    )
