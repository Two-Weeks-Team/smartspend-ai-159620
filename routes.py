from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from models import SessionLocal, get_db, Transaction, Category, User
from ai_service import call_inference

router = APIRouter()

# ---------------------------------------------------------------------------
# Pydantic schemas (simple, non‑recursive)
# ---------------------------------------------------------------------------
class TransactionInput(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    amount: float = Field(..., description="Transaction amount")
    description: str = Field(..., description="Raw transaction description")

class CategorizeRequest(BaseModel):
    transactions: List[TransactionInput]

class CategorizedItem(BaseModel):
    transaction_id: str
    category: str

class CategorizeResponse(BaseModel):
    categorized_transactions: List[CategorizedItem]

class BudgetRecommendationResponse(BaseModel):
    recommended_budget: dict

class InsightResponse(BaseModel):
    weekly_insights: dict
    monthly_insights: dict

# ---------------------------------------------------------------------------
# Helper – dummy user fetch (in a real app you would use auth middleware)
# ---------------------------------------------------------------------------
def _get_demo_user(db) -> User:
    # For demo purposes we either fetch the first user or create a placeholder
    user = db.query(User).first()
    if not user:
        from uuid import uuid4
        user = User(
            user_id=str(uuid4()),
            email="demo@example.com",
            password_hash="not_used",
            name="Demo User",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# ---------------------------------------------------------------------------
# AI‑powered endpoint: transaction categorization
# ---------------------------------------------------------------------------
@router.post("/transactions/categorize", response_model=CategorizeResponse)
async def categorize_transactions(payload: CategorizeRequest, db: SessionLocal = Depends(get_db)):
    # Build a prompt that lists transactions and asks the model to return JSON
    tx_list = [
        {"id": tx.transaction_id, "amount": tx.amount, "description": tx.description}
        for tx in payload.transactions
    ]
    user_msg = (
        "You are an expense categorization assistant. Given the list of transactions below, return a JSON array "
        "where each element contains 'transaction_id' and a concise 'category' string. Use the following format: "
        "```json\n[{'transaction_id': '...', 'category': '...'}, ...]\n```\n"
        f"Transactions: {json.dumps(tx_list)}"
    )
    messages = [{"role": "user", "content": user_msg}]
    raw_result = await call_inference(messages)
    # Expecting a dict with key 'categorized_transactions' or raw list
    if isinstance(raw_result, dict) and "categorized_transactions" in raw_result:
        cats = raw_result["categorized_transactions"]
    elif isinstance(raw_result, list):
        cats = raw_result
    else:
        # Fallback – mark all as 'Uncategorized'
        cats = [{"transaction_id": tx.transaction_id, "category": "Uncategorized"} for tx in payload.transactions]
    # Persist categories if needed (simple demo – create if not exists)
    user = _get_demo_user(db)
    for item in cats:
        cat_name = item.get("category", "Uncategorized")
        # Find or create category for the demo user
        cat = db.query(Category).filter_by(name=cat_name, user_id=user.user_id).first()
        if not cat:
            from uuid import uuid4
            cat = Category(
                category_id=str(uuid4()),
                user_id=user.user_id,
                name=cat_name,
                is_default=False,
            )
            db.add(cat)
            db.commit()
            db.refresh(cat)
        # Update transaction with category reference if transaction exists in DB (optional)
        tx = db.query(Transaction).filter_by(transaction_id=item["transaction_id"], user_id=user.user_id).first()
        if tx:
            tx.category_id = cat.category_id
            db.add(tx)
            db.commit()
    return CategorizeResponse(categorized_transactions=cats)

# ---------------------------------------------------------------------------
# AI‑powered endpoint: budget recommendations
# ---------------------------------------------------------------------------
@router.get("/budget/recommendations", response_model=BudgetRecommendationResponse)
async def budget_recommendations(db: SessionLocal = Depends(get_db)):
    user = _get_demo_user(db)
    prompt = (
        "You are a personal finance coach. Based on a typical user's spending patterns, provide a JSON object named "
        "'recommended_budget' with the following keys: income (number), expenses (object with categories "
        "like housing, food, transportation, entertainment – each a number), and savings (number). "
        "Make the numbers realistic and balanced."
    )
    messages = [{"role": "user", "content": prompt}]
    raw = await call_inference(messages)
    if isinstance(raw, dict) and "recommended_budget" in raw:
        budget = raw["recommended_budget"]
    else:
        # Fallback simple budget
        budget = {
            "income": 5000,
            "expenses": {"housing": 1500, "food": 600, "transportation": 300, "entertainment": 200},
            "savings": 1000,
        }
    return BudgetRecommendationResponse(recommended_budget=budget)

# ---------------------------------------------------------------------------
# AI‑powered endpoint: spending insights (weekly & monthly)
# ---------------------------------------------------------------------------
@router.get("/spending/insights", response_model=InsightResponse)
async def spending_insights(db: SessionLocal = Depends(get_db)):
    user = _get_demo_user(db)
    prompt = (
        "Provide weekly and monthly spending insights for a user in JSON format with keys 'weekly_insights' and "
        "'monthly_insights'. Weekly insights should include 'average_spending' and a list of 'top_categories' (each with "
        "'category' and 'amount'). Monthly insights should include 'total_spending' and a short 'trend_analysis' "
        "string describing the overall trend."
    )
    messages = [{"role": "user", "content": prompt}]
    raw = await call_inference(messages)
    if isinstance(raw, dict) and "weekly_insights" in raw and "monthly_insights" in raw:
        weekly = raw["weekly_insights"]
        monthly = raw["monthly_insights"]
    else:
        # Simple static fallback
        weekly = {
            "average_spending": 1200.0,
            "top_categories": [{"category": "Food", "amount": 300.0}, {"category": "Transport", "amount": 150.0}],
        }
        monthly = {
            "total_spending": 4800.0,
            "trend_analysis": "Spending is stable with a slight increase in entertainment.",
        }
    return InsightResponse(weekly_insights=weekly, monthly_insights=monthly)
