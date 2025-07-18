from typing import Optional
from datetime import datetime
from app.database.mongo import db

class NotifierService:
    @staticmethod
    async def send_notification(user_id: str, message: str) -> dict:
        notification = {
            "user_id": user_id,
            "message": message,
            "created_at": datetime.utcnow(),
            "read": False
        }
        result = await db.notifications.insert_one(notification)
        notification["_id"] = str(result.inserted_id)
        return notification

    @staticmethod
    async def mark_as_read(notification_id: str) -> bool:
        result = await db.notifications.update_one(
            {"_id": notification_id}, {"$set": {"read": True}}
        )
        return result.modified_count > 0
