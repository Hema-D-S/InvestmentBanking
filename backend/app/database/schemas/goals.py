from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class GoalSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: Optional[date]
    status: Optional[str] = "active"  # e.g., active, completed, archived

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
