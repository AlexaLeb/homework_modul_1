from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class PredictionHistory(SQLModel, table=True):
    __tablename__ = "prediction_histories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    details: Optional[str] = Field(default=None, nullable=True)  # Детали предсказания (например, JSON)
    timestamp: datetime = Field(default_factory=datetime.now)

