from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from app.database.schemas.investments import InvestmentSchema
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=InvestmentSchema, status_code=status.HTTP_201_CREATED)
async def create_investment(investment: InvestmentSchema):
    investment_dict = investment.dict(by_alias=True, exclude_unset=True)
    result = await db.investments.insert_one(investment_dict)
    investment_dict["_id"] = str(result.inserted_id)
    return investment_dict

@router.get("/", response_model=List[InvestmentSchema])
async def list_investments(user_id: str):
    investments = await db.investments.find({"user_id": user_id}).to_list(100)
    for i in investments:
        i["_id"] = str(i["_id"])
    return investments

@router.get("/{investment_id}", response_model=InvestmentSchema)
async def get_investment(investment_id: str):
    investment = await db.investments.find_one({"_id": ObjectId(investment_id)})
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    investment["_id"] = str(investment["_id"])
    return investment

@router.put("/{investment_id}", response_model=InvestmentSchema)
async def update_investment(investment_id: str, investment: InvestmentSchema):
    update_data = {k: v for k, v in investment.dict(exclude_unset=True).items() if v is not None}
    result = await db.investments.update_one({"_id": ObjectId(investment_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Investment not found or not updated")
    updated_investment = await db.investments.find_one({"_id": ObjectId(investment_id)})
    updated_investment["_id"] = str(updated_investment["_id"])
    return updated_investment

@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investment(investment_id: str):
    result = await db.investments.delete_one({"_id": ObjectId(investment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Investment not found")
    return None
