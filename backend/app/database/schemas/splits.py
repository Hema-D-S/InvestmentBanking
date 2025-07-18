from pydantic import BaseModel, Field
from typing import Optional, List

class SplitSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    group_id: str
    payer_id: str
    amount: float
    participants: List[str]  # user IDs
    description: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
