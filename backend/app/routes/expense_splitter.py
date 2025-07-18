from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from app.database.schemas.splits import SplitSchema
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=SplitSchema, status_code=status.HTTP_201_CREATED)
async def create_split(split: SplitSchema):
    split_dict = split.dict(by_alias=True, exclude_unset=True)
    result = await db.splits.insert_one(split_dict)
    split_dict["_id"] = str(result.inserted_id)
    return split_dict

@router.get("/", response_model=List[SplitSchema])
async def list_splits(group_id: str):
    splits = await db.splits.find({"group_id": group_id}).to_list(100)
    for s in splits:
        s["_id"] = str(s["_id"])
    return splits

@router.get("/{split_id}", response_model=SplitSchema)
async def get_split(split_id: str):
    split = await db.splits.find_one({"_id": ObjectId(split_id)})
    if not split:
        raise HTTPException(status_code=404, detail="Split not found")
    split["_id"] = str(split["_id"])
    return split

@router.put("/{split_id}", response_model=SplitSchema)
async def update_split(split_id: str, split: SplitSchema):
    update_data = {k: v for k, v in split.dict(exclude_unset=True).items() if v is not None}
    result = await db.splits.update_one({"_id": ObjectId(split_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Split not found or not updated")
    updated_split = await db.splits.find_one({"_id": ObjectId(split_id)})
    updated_split["_id"] = str(updated_split["_id"])
    return updated_split

@router.delete("/{split_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_split(split_id: str):
    result = await db.splits.delete_one({"_id": ObjectId(split_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Split not found")
    return None
