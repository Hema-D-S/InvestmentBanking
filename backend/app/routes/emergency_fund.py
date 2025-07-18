from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class EmergencyFundSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    target_amount: float
    current_amount: float = 0.0
    created_at: Optional[str]
    status: Optional[str] = "active"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

router = APIRouter()

@router.post("/", response_model=EmergencyFundSchema, status_code=status.HTTP_201_CREATED)
async def create_emergency_fund(fund: EmergencyFundSchema):
    fund_dict = fund.dict(by_alias=True, exclude_unset=True)
    result = await db.emergency_funds.insert_one(fund_dict)
    fund_dict["_id"] = str(result.inserted_id)
    return fund_dict

@router.get("/", response_model=List[EmergencyFundSchema])
async def list_emergency_funds(user_id: str):
    funds = await db.emergency_funds.find({"user_id": user_id}).to_list(100)
    for f in funds:
        f["_id"] = str(f["_id"])
    return funds

@router.get("/{fund_id}", response_model=EmergencyFundSchema)
async def get_emergency_fund(fund_id: str):
    fund = await db.emergency_funds.find_one({"_id": ObjectId(fund_id)})
    if not fund:
        raise HTTPException(status_code=404, detail="Emergency fund not found")
    fund["_id"] = str(fund["_id"])
    return fund

@router.put("/{fund_id}", response_model=EmergencyFundSchema)
async def update_emergency_fund(fund_id: str, fund: EmergencyFundSchema):
    update_data = {k: v for k, v in fund.dict(exclude_unset=True).items() if v is not None}
    result = await db.emergency_funds.update_one({"_id": ObjectId(fund_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Emergency fund not found or not updated")
    updated_fund = await db.emergency_funds.find_one({"_id": ObjectId(fund_id)})
    updated_fund["_id"] = str(updated_fund["_id"])
    return updated_fund

@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emergency_fund(fund_id: str):
    result = await db.emergency_funds.delete_one({"_id": ObjectId(fund_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Emergency fund not found")
    return None
