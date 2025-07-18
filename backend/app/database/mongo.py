from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "investment_banking")

client = AsyncIOMotorClient(MONGO_URL)
db: Database = client[DATABASE_NAME]
