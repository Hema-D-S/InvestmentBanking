from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
