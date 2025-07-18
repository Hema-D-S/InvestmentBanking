from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class NotificationSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    message: str
    created_at: datetime
    read: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

router = APIRouter()

@router.post("/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED)
async def create_notification(notification: NotificationSchema):
    notification_dict = notification.dict(by_alias=True, exclude_unset=True)
    result = await db.notifications.insert_one(notification_dict)
    notification_dict["_id"] = str(result.inserted_id)
    return notification_dict

@router.get("/", response_model=List[NotificationSchema])
async def list_notifications(user_id: str):
    notifications = await db.notifications.find({"user_id": user_id}).to_list(100)
    for n in notifications:
        n["_id"] = str(n["_id"])
    return notifications

@router.get("/{notification_id}", response_model=NotificationSchema)
async def get_notification(notification_id: str):
    notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification["_id"] = str(notification["_id"])
    return notification

@router.put("/{notification_id}", response_model=NotificationSchema)
async def update_notification(notification_id: str, notification: NotificationSchema):
    update_data = {k: v for k, v in notification.dict(exclude_unset=True).items() if v is not None}
    result = await db.notifications.update_one({"_id": ObjectId(notification_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found or not updated")
    updated_notification = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    updated_notification["_id"] = str(updated_notification["_id"])
    return updated_notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: str):
    result = await db.notifications.delete_one({"_id": ObjectId(notification_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return None
