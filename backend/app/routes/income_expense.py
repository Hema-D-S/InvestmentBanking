from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from app.database.schemas.transactions import TransactionSchema
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionSchema):
    transaction_dict = transaction.dict(by_alias=True, exclude_unset=True)
    result = await db.transactions.insert_one(transaction_dict)
    transaction_dict["_id"] = str(result.inserted_id)
    return transaction_dict

@router.get("/", response_model=List[TransactionSchema])
async def list_transactions(user_id: str):
    transactions = await db.transactions.find({"user_id": user_id}).to_list(100)
    for t in transactions:
        t["_id"] = str(t["_id"])
    return transactions

@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(transaction_id: str):
    transaction = await db.transactions.find_one({"_id": ObjectId(transaction_id)})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction["_id"] = str(transaction["_id"])
    return transaction

@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(transaction_id: str, transaction: TransactionSchema):
    update_data = {k: v for k, v in transaction.dict(exclude_unset=True).items() if v is not None}
    result = await db.transactions.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found or not updated")
    updated_transaction = await db.transactions.find_one({"_id": ObjectId(transaction_id)})
    updated_transaction["_id"] = str(updated_transaction["_id"])
    return updated_transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str):
    result = await db.transactions.delete_one({"_id": ObjectId(transaction_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None
