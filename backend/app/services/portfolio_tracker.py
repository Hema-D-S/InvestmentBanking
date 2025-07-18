from app.database.mongo import db
from typing import List

class PortfolioTrackerService:
    @staticmethod
    async def get_total_investment_value(user_id: str) -> float:
        investments = await db.investments.find({"user_id": user_id}).to_list(100)
        total = sum(inv.get("amount", 0) for inv in investments)
        return round(total, 2)

    @staticmethod
    async def list_investments(user_id: str) -> List[dict]:
        investments = await db.investments.find({"user_id": user_id}).to_list(100)
        for inv in investments:
            inv["_id"] = str(inv["_id"])
        return investments
