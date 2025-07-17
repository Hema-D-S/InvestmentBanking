from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database.database import get_db
from app.database.models import User, Transaction
from app.utils.auth import get_current_active_user
from app.utils.schemas import (
    TransactionCreate, 
    Transaction as TransactionSchema, 
    TransactionUpdate,
    PaginatedResponse
)

router = APIRouter()

@router.post("/", response_model=TransactionSchema)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction"""
    db_transaction = Transaction(
        user_id=current_user.id,
        amount=transaction.amount,
        description=transaction.description,
        category=transaction.category.value,
        transaction_type=transaction.transaction_type.value,
        date=transaction.date or datetime.utcnow(),
        is_recurring=transaction.is_recurring,
        recurring_frequency=transaction.recurring_frequency
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

@router.get("/", response_model=PaginatedResponse)
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get paginated transactions with optional filters"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    if category:
        query = query.filter(Transaction.category == category)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    total = query.count()
    transactions = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[transaction.__dict__ for transaction in transactions],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific transaction"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction

@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a transaction"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    update_data = transaction_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "category" and value:
            setattr(transaction, field, value.value)
        elif field == "transaction_type" and value:
            setattr(transaction, field, value.value)
        else:
            setattr(transaction, field, value)
    
    db.commit()
    db.refresh(transaction)
    
    return transaction

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a transaction"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}

@router.get("/summary/current-month")
async def get_current_month_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current month financial summary"""
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_of_month
    ).all()
    
    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
    net_income = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": net_income,
        "savings_rate": (net_income / total_income * 100) if total_income > 0 else 0
    }

@router.get("/categories/summary")
async def get_category_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get spending summary by category"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.all()
    
    category_summary = {}
    for transaction in transactions:
        category = transaction.category
        if category not in category_summary:
            category_summary[category] = {"income": 0, "expense": 0}
        
        if transaction.transaction_type == "income":
            category_summary[category]["income"] += transaction.amount
        else:
            category_summary[category]["expense"] += transaction.amount
    
    return category_summary 