from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(str, Enum):
    SALARY = "salary"
    INVESTMENT = "investment"
    BUSINESS = "business"
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    HEALTH = "health"
    EDUCATION = "education"
    UTILITIES = "utilities"
    RENT = "rent"
    OTHER = "other"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Transaction schemas
class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category: TransactionCategory
    transaction_type: TransactionType
    date: Optional[datetime] = None
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[TransactionCategory] = None
    transaction_type: Optional[TransactionType] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_frequency: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Savings Goal schemas
class SavingsGoalBase(BaseModel):
    name: str
    target_amount: float
    target_date: Optional[datetime] = None
    description: Optional[str] = None

class SavingsGoalCreate(SavingsGoalBase):
    pass

class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class SavingsGoal(SavingsGoalBase):
    id: int
    user_id: int
    current_amount: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Report schemas
class ReportBase(BaseModel):
    report_type: str
    report_data: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    user_id: int
    generated_at: datetime

    class Config:
        from_attributes = True

# Advisor Recommendation schemas
class AdvisorRecommendationBase(BaseModel):
    recommendation_type: str
    title: str
    description: str
    priority: Priority

class AdvisorRecommendationCreate(AdvisorRecommendationBase):
    pass

class AdvisorRecommendationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    is_implemented: Optional[bool] = None

class AdvisorRecommendation(AdvisorRecommendationBase):
    id: int
    user_id: int
    is_implemented: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Financial Summary schemas
class FinancialSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_income: float
    savings_rate: float
    monthly_trend: List[dict]
    category_breakdown: List[dict]

# Response schemas
class Message(BaseModel):
    message: str

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int 