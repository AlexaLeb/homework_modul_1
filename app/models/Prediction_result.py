from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class PredictionResult(SQLModel, table=True):
    __tablename__ = "prediction_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="prediction_tasks.id")
    recommended_distribution: str = Field(..., nullable=False)
    timestamp: datetime = Field(default_factory=datetime.now)

    task: Optional["PredictionTask"] = Relationship(back_populates="result")
