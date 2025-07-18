from app.database.mongo import db
from app.database.schemas.goals import GoalSchema
from typing import Optional
from bson import ObjectId
from datetime import datetime

class GoalManagerService:
    @staticmethod
    async def create_goal(goal: GoalSchema) -> dict:
        goal_dict = goal.dict(by_alias=True, exclude_unset=True)
        result = await db.goals.insert_one(goal_dict)
        goal_dict["_id"] = str(result.inserted_id)
        return goal_dict

    @staticmethod
    async def update_goal(goal_id: str, update_data: dict) -> Optional[dict]:
        result = await db.goals.update_one({"_id": ObjectId(goal_id)}, {"$set": update_data})
        if result.modified_count == 0:
            return None
        updated_goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        updated_goal["_id"] = str(updated_goal["_id"])
        return updated_goal

    @staticmethod
    async def mark_goal_completed(goal_id: str) -> Optional[dict]:
        result = await db.goals.update_one({"_id": ObjectId(goal_id)}, {"$set": {"status": "completed", "completed_at": datetime.utcnow()}})
        if result.modified_count == 0:
            return None
        updated_goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        updated_goal["_id"] = str(updated_goal["_id"])
        return updated_goal
