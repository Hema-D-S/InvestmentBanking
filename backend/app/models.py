from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: Optional[str]
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str 