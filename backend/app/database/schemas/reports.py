from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReportSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    period: str  # e.g., '2024-Q1', '2024-07'
    generated_at: datetime
    summary: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
