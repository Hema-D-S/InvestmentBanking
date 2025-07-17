from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
import json
import pandas as pd
from app.database.database import get_db
from app.database.models import User, Transaction, Report
from app.utils.auth import get_current_active_user
from app.utils.schemas import ReportCreate, Report as ReportSchema, FinancialSummary

router = APIRouter()

@router.get("/financial-summary")
async def get_financial_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive financial summary"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.all()
    
    if not transactions:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "net_income": 0,
            "savings_rate": 0,
            "monthly_trend": [],
            "category_breakdown": []
        }
    
    # Calculate basic metrics
    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
    net_income = total_income - total_expenses
    savings_rate = (net_income / total_income * 100) if total_income > 0 else 0
    
    # Monthly trend analysis
    monthly_data = {}
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {"income": 0, "expense": 0}
        
        if transaction.transaction_type == "income":
            monthly_data[month_key]["income"] += transaction.amount
        else:
            monthly_data[month_key]["expense"] += transaction.amount
    
    monthly_trend = [
        {
            "month": month,
            "income": data["income"],
            "expense": data["expense"],
            "net": data["income"] - data["expense"]
        }
        for month, data in monthly_data.items()
    ]
    
    # Category breakdown
    category_data = {}
    for transaction in transactions:
        category = transaction.category
        if category not in category_data:
            category_data[category] = {"income": 0, "expense": 0}
        
        if transaction.transaction_type == "income":
            category_data[category]["income"] += transaction.amount
        else:
            category_data[category]["expense"] += transaction.amount
    
    category_breakdown = [
        {
            "category": category,
            "income": data["income"],
            "expense": data["expense"],
            "net": data["income"] - data["expense"]
        }
        for category, data in category_data.items()
    ]
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": net_income,
        "savings_rate": savings_rate,
        "monthly_trend": monthly_trend,
        "category_breakdown": category_breakdown
    }

@router.get("/spending-analysis")
async def get_spending_analysis(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed spending analysis for the last N months"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.transaction_type == "expense"
    ).all()
    
    if not transactions:
        return {
            "total_spending": 0,
            "average_monthly_spending": 0,
            "top_categories": [],
            "spending_trend": []
        }
    
    # Calculate spending metrics
    total_spending = sum(t.amount for t in transactions)
    average_monthly_spending = total_spending / months
    
    # Top spending categories
    category_spending = {}
    for transaction in transactions:
        category = transaction.category
        category_spending[category] = category_spending.get(category, 0) + transaction.amount
    
    top_categories = sorted(
        [{"category": cat, "amount": amt} for cat, amt in category_spending.items()],
        key=lambda x: x["amount"],
        reverse=True
    )[:5]
    
    # Spending trend by month
    monthly_spending = {}
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")
        monthly_spending[month_key] = monthly_spending.get(month_key, 0) + transaction.amount
    
    spending_trend = [
        {"month": month, "amount": amount}
        for month, amount in monthly_spending.items()
    ]
    
    return {
        "total_spending": total_spending,
        "average_monthly_spending": average_monthly_spending,
        "top_categories": top_categories,
        "spending_trend": spending_trend
    }

@router.get("/income-analysis")
async def get_income_analysis(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed income analysis for the last N months"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=months * 30)
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.transaction_type == "income"
    ).all()
    
    if not transactions:
        return {
            "total_income": 0,
            "average_monthly_income": 0,
            "income_sources": [],
            "income_trend": []
        }
    
    # Calculate income metrics
    total_income = sum(t.amount for t in transactions)
    average_monthly_income = total_income / months
    
    # Income sources breakdown
    source_income = {}
    for transaction in transactions:
        category = transaction.category
        source_income[category] = source_income.get(category, 0) + transaction.amount
    
    income_sources = sorted(
        [{"source": source, "amount": amt} for source, amt in source_income.items()],
        key=lambda x: x["amount"],
        reverse=True
    )
    
    # Income trend by month
    monthly_income = {}
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")
        monthly_income[month_key] = monthly_income.get(month_key, 0) + transaction.amount
    
    income_trend = [
        {"month": month, "amount": amount}
        for month, amount in monthly_income.items()
    ]
    
    return {
        "total_income": total_income,
        "average_monthly_income": average_monthly_income,
        "income_sources": income_sources,
        "income_trend": income_trend
    }

@router.post("/generate", response_model=ReportSchema)
async def generate_report(
    report_type: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate and save a custom report"""
    # Generate report data based on type
    if report_type == "monthly":
        end_date = datetime.utcnow()
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif report_type == "yearly":
        end_date = datetime.utcnow()
        start_date = end_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get financial summary for the period
    summary = await get_financial_summary(start_date, end_date, current_user, db)
    
    # Create report record
    report = Report(
        user_id=current_user.id,
        report_type=report_type,
        report_data=json.dumps(summary)
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report

@router.get("/saved", response_model=List[ReportSchema])
async def get_saved_reports(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all saved reports for the current user"""
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).order_by(Report.generated_at.desc()).all()
    
    return reports

@router.get("/saved/{report_id}", response_model=ReportSchema)
async def get_saved_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific saved report"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report 