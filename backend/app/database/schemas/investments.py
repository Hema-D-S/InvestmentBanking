from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class InvestmentSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    type: str  # e.g., stock, bond, mutual fund
    amount: float
    date: date
    status: Optional[str] = "active"  # e.g., active, sold, matured

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
