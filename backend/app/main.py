from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from app.routes import auth, transactions, reports, advisor, user
from app.database.database import init_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Investment Banking Platform starting up...")
    await init_db()
    yield
    print("👋 Investment Banking Platform shutting down...")

app = FastAPI(
    title="Investment Banking Platform",
    description="A comprehensive investment banking platform with income/expense tracking, savings advisor, and advanced reporting capabilities.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(advisor.router, prefix="/api/advisor", tags=["Savings Advisor"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Investment Banking Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "Income/Expense Tracking",
            "Savings Advisor",
            "Report Engine"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Investment Banking Platform"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
