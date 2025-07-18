from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from app.database.schemas.goals import GoalSchema
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=GoalSchema, status_code=status.HTTP_201_CREATED)
async def create_goal(goal: GoalSchema):
    goal_dict = goal.dict(by_alias=True, exclude_unset=True)
    result = await db.goals.insert_one(goal_dict)
    goal_dict["_id"] = str(result.inserted_id)
    return goal_dict

@router.get("/", response_model=List[GoalSchema])
async def list_goals():
    goals = await db.goals.find().to_list(100)
    for g in goals:
        g["_id"] = str(g["_id"])
    return goals

@router.get("/{goal_id}", response_model=GoalSchema)
async def get_goal(goal_id: str):
    goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal["_id"] = str(goal["_id"])
    return goal

@router.put("/{goal_id}", response_model=GoalSchema)
async def update_goal(goal_id: str, goal: GoalSchema):
    update_data = {k: v for k, v in goal.dict(exclude_unset=True).items() if v is not None}
    result = await db.goals.update_one({"_id": ObjectId(goal_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found or not updated")
    updated_goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
    updated_goal["_id"] = str(updated_goal["_id"])
    return updated_goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: str):
    result = await db.goals.delete_one({"_id": ObjectId(goal_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return None
