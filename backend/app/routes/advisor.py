from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database.database import get_db
from app.database.models import User, Transaction, SavingsGoal, AdvisorRecommendation
from app.utils.auth import get_current_active_user
from app.utils.schemas import (
    SavingsGoalCreate, 
    SavingsGoal as SavingsGoalSchema, 
    SavingsGoalUpdate,
    AdvisorRecommendationCreate,
    AdvisorRecommendation as AdvisorRecommendationSchema,
    AdvisorRecommendationUpdate
)

router = APIRouter()

@router.post("/savings-goals", response_model=SavingsGoalSchema)
async def create_savings_goal(
    goal: SavingsGoalCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new savings goal"""
    db_goal = SavingsGoal(
        user_id=current_user.id,
        name=goal.name,
        target_amount=goal.target_amount,
        target_date=goal.target_date,
        description=goal.description
    )
    
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    return db_goal

@router.get("/savings-goals", response_model=List[SavingsGoalSchema])
async def get_savings_goals(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all savings goals for the current user"""
    goals = db.query(SavingsGoal).filter(
        SavingsGoal.user_id == current_user.id
    ).order_by(SavingsGoal.created_at.desc()).all()
    
    return goals

@router.get("/savings-goals/{goal_id}", response_model=SavingsGoalSchema)
async def get_savings_goal(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific savings goal"""
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found"
        )
    
    return goal

@router.put("/savings-goals/{goal_id}", response_model=SavingsGoalSchema)
async def update_savings_goal(
    goal_id: int,
    goal_update: SavingsGoalUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a savings goal"""
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found"
        )
    
    update_data = goal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    
    return goal

@router.delete("/savings-goals/{goal_id}")
async def delete_savings_goal(
    goal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a savings goal"""
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found"
        )
    
    db.delete(goal)
    db.commit()
    
    return {"message": "Savings goal deleted successfully"}

@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered financial recommendations"""
    # Get user's financial data
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).all()
    
    if not transactions:
        return {
            "recommendations": [
                {
                    "type": "savings",
                    "title": "Start Tracking Your Finances",
                    "description": "Begin by adding your first income and expense transactions to get personalized recommendations.",
                    "priority": "high"
                }
            ]
        }
    
    # Calculate financial metrics
    total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
    net_income = total_income - total_expenses
    savings_rate = (net_income / total_income * 100) if total_income > 0 else 0
    
    # Generate recommendations based on financial data
    recommendations = []
    
    # Savings rate recommendations
    if savings_rate < 20:
        recommendations.append({
            "type": "savings",
            "title": "Increase Your Savings Rate",
            "description": f"Your current savings rate is {savings_rate:.1f}%. Aim to save at least 20% of your income for better financial security.",
            "priority": "high"
        })
    elif savings_rate < 30:
        recommendations.append({
            "type": "savings",
            "title": "Optimize Your Savings",
            "description": f"Great job! Your savings rate is {savings_rate:.1f}%. Consider increasing it to 30% for accelerated wealth building.",
            "priority": "medium"
        })
    else:
        recommendations.append({
            "type": "savings",
            "title": "Excellent Savings Rate",
            "description": f"Outstanding! Your {savings_rate:.1f}% savings rate is excellent. Consider investing your surplus for long-term growth.",
            "priority": "low"
        })
    
    # Spending analysis
    category_spending = {}
    for transaction in transactions:
        if transaction.transaction_type == "expense":
            category = transaction.category
            category_spending[category] = category_spending.get(category, 0) + transaction.amount
    
    # Identify high spending categories
    if category_spending:
        top_spending_category = max(category_spending.items(), key=lambda x: x[1])
        if top_spending_category[1] > total_income * 0.3:  # More than 30% of income
            recommendations.append({
                "type": "budget",
                "title": "Review High Spending Category",
                "description": f"Your {top_spending_category[0]} spending is {top_spending_category[1]:.0f}, which is over 30% of your income. Consider reducing expenses in this category.",
                "priority": "high"
            })
    
    # Emergency fund recommendation
    if net_income > 0:
        monthly_expenses = total_expenses / 12 if len(transactions) >= 12 else total_expenses
        emergency_fund_needed = monthly_expenses * 6
        
        recommendations.append({
            "type": "emergency_fund",
            "title": "Build Emergency Fund",
            "description": f"Consider building an emergency fund of ${emergency_fund_needed:.0f} (6 months of expenses) for financial security.",
            "priority": "medium"
        })
    
    # Investment recommendations
    if savings_rate > 25:
        recommendations.append({
            "type": "investment",
            "title": "Consider Investment Opportunities",
            "description": "With your strong savings rate, consider diversifying into investment vehicles for long-term wealth building.",
            "priority": "medium"
        })
    
    return {"recommendations": recommendations}

@router.post("/recommendations", response_model=AdvisorRecommendationSchema)
async def create_recommendation(
    recommendation: AdvisorRecommendationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a custom recommendation"""
    db_recommendation = AdvisorRecommendation(
        user_id=current_user.id,
        recommendation_type=recommendation.recommendation_type,
        title=recommendation.title,
        description=recommendation.description,
        priority=recommendation.priority.value
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation

@router.get("/recommendations/saved", response_model=List[AdvisorRecommendationSchema])
async def get_saved_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all saved recommendations for the current user"""
    recommendations = db.query(AdvisorRecommendation).filter(
        AdvisorRecommendation.user_id == current_user.id
    ).order_by(AdvisorRecommendation.created_at.desc()).all()
    
    return recommendations

@router.put("/recommendations/{recommendation_id}", response_model=AdvisorRecommendationSchema)
async def update_recommendation(
    recommendation_id: int,
    recommendation_update: AdvisorRecommendationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a recommendation"""
    recommendation = db.query(AdvisorRecommendation).filter(
        AdvisorRecommendation.id == recommendation_id,
        AdvisorRecommendation.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    update_data = recommendation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "priority" and value:
            setattr(recommendation, field, value.value)
        else:
            setattr(recommendation, field, value)
    
    db.commit()
    db.refresh(recommendation)
    
    return recommendation

@router.get("/savings-calculator")
async def calculate_savings_plan(
    target_amount: float = Query(..., gt=0),
    target_date: datetime = Query(...),
    current_monthly_income: float = Query(..., gt=0),
    current_monthly_expenses: float = Query(..., ge=0),
    current_user: User = Depends(get_current_active_user)
):
    """Calculate savings plan to reach a financial goal"""
    months_to_target = (target_date.year - datetime.utcnow().year) * 12 + (target_date.month - datetime.utcnow().month)
    
    if months_to_target <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target date must be in the future"
        )
    
    monthly_savings_needed = target_amount / months_to_target
    available_for_savings = current_monthly_income - current_monthly_expenses
    
    if available_for_savings < monthly_savings_needed:
        # Need to reduce expenses or increase income
        additional_needed = monthly_savings_needed - available_for_savings
        return {
            "target_amount": target_amount,
            "months_to_target": months_to_target,
            "monthly_savings_needed": monthly_savings_needed,
            "available_for_savings": available_for_savings,
            "additional_needed": additional_needed,
            "feasible": False,
            "recommendations": [
                f"Increase income by ${additional_needed:.2f} per month, or",
                f"Reduce expenses by ${additional_needed:.2f} per month, or",
                f"Extend your target date by {int(additional_needed / monthly_savings_needed * months_to_target)} months"
            ]
        }
    else:
        return {
            "target_amount": target_amount,
            "months_to_target": months_to_target,
            "monthly_savings_needed": monthly_savings_needed,
            "available_for_savings": available_for_savings,
            "surplus": available_for_savings - monthly_savings_needed,
            "feasible": True,
            "recommendations": [
                "Your goal is achievable with your current financial situation!",
                f"You can save ${monthly_savings_needed:.2f} per month to reach your goal.",
                f"You'll have ${available_for_savings - monthly_savings_needed:.2f} surplus for other goals."
            ]
        } 