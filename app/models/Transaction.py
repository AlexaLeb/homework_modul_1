from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    transaction_type: str = Field(..., nullable=False)  # Например, "deposit", "withdrawal" и т.п.
    amount: float = Field(..., nullable=False)
    timestamp: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="transactions")
