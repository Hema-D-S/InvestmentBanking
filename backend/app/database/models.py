from beanie import Document, Link
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(str, enum.Enum):
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

class User(Document):
    email: EmailStr
    username: str
    hashed_password: str
    full_name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"

class Transaction(Document):
    user: Link[User]
    amount: float
    description: Optional[str] = None
    category: str
    transaction_type: str  # income or expense
    date: datetime = Field(default_factory=datetime.utcnow)
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "transactions"

class SavingsGoal(Document):
    user: Link[User]
    name: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[datetime] = None
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "savings_goals"

class Report(Document):
    user: Link[User]
    report_type: str  # monthly, yearly, custom
    report_data: str  # JSON string of report data
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reports"

class AdvisorRecommendation(Document):
    user: Link[User]
    recommendation_type: str  # savings, investment, budget
    title: str
    description: str
    priority: str  # high, medium, low
    is_implemented: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "advisor_recommendations" 