import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.database.models import User, Transaction, SavingsGoal, Report, AdvisorRecommendation

MONGODB_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/investment_banking")

# Database connection and initialization
async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_default_database()
    await init_beanie(
        database=db,
        document_models=[User, Transaction, SavingsGoal, Report, AdvisorRecommendation]
    )
    return db  # Return the database instance

# Add this function for dependency injection
async def get_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        db = client.get_default_database()
        yield db
    finally:
        client.close()