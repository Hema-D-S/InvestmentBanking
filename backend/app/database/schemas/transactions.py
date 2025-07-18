from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    type: str  # e.g., income, expense, transfer
    amount: float
    date: datetime
    description: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
