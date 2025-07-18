from app.database.mongo import db
from typing import List, Dict

class IncomeExpenseService:
    @staticmethod
    async def add_transaction(transaction: dict) -> dict:
        result = await db.transactions.insert_one(transaction)
        transaction["_id"] = str(result.inserted_id)
        return transaction

    @staticmethod
    async def list_transactions(user_id: str) -> List[dict]:
        transactions = await db.transactions.find({"user_id": user_id}).to_list(100)
        for t in transactions:
            t["_id"] = str(t["_id"])
        return transactions

    @staticmethod
    async def summarize(user_id: str) -> Dict[str, float]:
        transactions = await db.transactions.find({"user_id": user_id}).to_list(1000)
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        return {"total_income": income, "total_expense": expense, "net": income - expense}
