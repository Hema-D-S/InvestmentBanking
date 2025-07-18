from datetime import datetime
from app.database.mongo import db
from typing import Optional

class ReportGeneratorService:
    @staticmethod
    async def generate_report(user_id: str, period: str, summary: str) -> dict:
        report = {
            "user_id": user_id,
            "period": period,
            "generated_at": datetime.utcnow(),
            "summary": summary
        }
        result = await db.reports.insert_one(report)
        report["_id"] = str(result.inserted_id)
        return report

    @staticmethod
    async def get_report(report_id: str) -> Optional[dict]:
        report = await db.reports.find_one({"_id": report_id})
        if report:
            report["_id"] = str(report["_id"])
        return report
