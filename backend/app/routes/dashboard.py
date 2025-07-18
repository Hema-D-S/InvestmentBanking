from fastapi import APIRouter, HTTPException, Depends
from app.database.mongo import db
from typing import Dict

router = APIRouter()

@router.get("/", response_model=Dict)
async def get_dashboard_summary(user_id: str):
    # Example: Aggregate user data for dashboard
    goals = await db.goals.count_documents({"user_id": user_id})
    investments = await db.investments.count_documents({"user_id": user_id})
    transactions = await db.transactions.count_documents({"user_id": user_id})
    reports = await db.reports.count_documents({"user_id": user_id})
    return {
        "goals_count": goals,
        "investments_count": investments,
        "transactions_count": transactions,
        "reports_count": reports
    }
