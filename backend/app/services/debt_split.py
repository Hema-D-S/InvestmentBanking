from typing import List, Dict
from app.database.mongo import db

class DebtSplitService:
    @staticmethod
    async def split_debt(group_id: str, payer_id: str, amount: float, participants: List[str], description: str = "") -> dict:
        if not participants:
            raise ValueError("Participants list cannot be empty.")
        share = round(amount / len(participants), 2)
        split = {
            "group_id": group_id,
            "payer_id": payer_id,
            "amount": amount,
            "participants": participants,
            "description": description,
            "share_per_person": share
        }
        result = await db.splits.insert_one(split)
        split["_id"] = str(result.inserted_id)
        return split
