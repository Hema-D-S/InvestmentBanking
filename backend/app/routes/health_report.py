from fastapi import APIRouter, HTTPException, status
from app.database.mongo import db
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class HealthReportSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    report_date: datetime
    score: float
    summary: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

router = APIRouter()

@router.post("/", response_model=HealthReportSchema, status_code=status.HTTP_201_CREATED)
async def create_health_report(report: HealthReportSchema):
    report_dict = report.dict(by_alias=True, exclude_unset=True)
    result = await db.health_reports.insert_one(report_dict)
    report_dict["_id"] = str(result.inserted_id)
    return report_dict

@router.get("/", response_model=List[HealthReportSchema])
async def list_health_reports(user_id: str):
    reports = await db.health_reports.find({"user_id": user_id}).to_list(100)
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports

@router.get("/{report_id}", response_model=HealthReportSchema)
async def get_health_report(report_id: str):
    report = await db.health_reports.find_one({"_id": ObjectId(report_id)})
    if not report:
        raise HTTPException(status_code=404, detail="Health report not found")
    report["_id"] = str(report["_id"])
    return report

@router.put("/{report_id}", response_model=HealthReportSchema)
async def update_health_report(report_id: str, report: HealthReportSchema):
    update_data = {k: v for k, v in report.dict(exclude_unset=True).items() if v is not None}
    result = await db.health_reports.update_one({"_id": ObjectId(report_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Health report not found or not updated")
    updated_report = await db.health_reports.find_one({"_id": ObjectId(report_id)})
    updated_report["_id"] = str(updated_report["_id"])
    return updated_report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_health_report(report_id: str):
    result = await db.health_reports.delete_one({"_id": ObjectId(report_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Health report not found")
    return None
