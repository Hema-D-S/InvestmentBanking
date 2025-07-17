import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.database import models

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/investment_banking")

async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_default_database()
    await init_beanie(
        database=db,
        document_models=[
            models.User,
            models.Transaction,
            models.SavingsGoal,
            models.Report,
            models.AdvisorRecommendation
        ]
    ) 