from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class SavingsAdviceSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    advice: str
    created_at: datetime
    read: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

router = APIRouter()

@router.post("/", response_model=SavingsAdviceSchema, status_code=status.HTTP_201_CREATED)
async def create_savings_advice(advice: SavingsAdviceSchema):
    advice_dict = advice.dict(by_alias=True, exclude_unset=True)
    result = await db.savings_advice.insert_one(advice_dict)
    advice_dict["_id"] = str(result.inserted_id)
    return advice_dict

@router.get("/", response_model=List[SavingsAdviceSchema])
async def list_savings_advice(user_id: str):
    advice_list = await db.savings_advice.find({"user_id": user_id}).to_list(100)
    for a in advice_list:
        a["_id"] = str(a["_id"])
    return advice_list

@router.get("/{advice_id}", response_model=SavingsAdviceSchema)
async def get_savings_advice(advice_id: str):
    advice = await db.savings_advice.find_one({"_id": ObjectId(advice_id)})
    if not advice:
        raise HTTPException(status_code=404, detail="Savings advice not found")
    advice["_id"] = str(advice["_id"])
    return advice

@router.put("/{advice_id}", response_model=SavingsAdviceSchema)
async def update_savings_advice(advice_id: str, advice: SavingsAdviceSchema):
    update_data = {k: v for k, v in advice.dict(exclude_unset=True).items() if v is not None}
    result = await db.savings_advice.update_one({"_id": ObjectId(advice_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Savings advice not found or not updated")
    updated_advice = await db.savings_advice.find_one({"_id": ObjectId(advice_id)})
    updated_advice["_id"] = str(updated_advice["_id"])
    return updated_advice

@router.delete("/{advice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_savings_advice(advice_id: str):
    result = await db.savings_advice.delete_one({"_id": ObjectId(advice_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Savings advice not found")
    return None
