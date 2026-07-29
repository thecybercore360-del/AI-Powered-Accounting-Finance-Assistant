import os

base = 'd:/Development/AI_Accounting_Assistant_Intern_Assignment_29July/ai-accounting-assistant/backend'

os.makedirs(f'{base}/core', exist_ok=True)
os.makedirs(f'{base}/models', exist_ok=True)
os.makedirs(f'{base}/schemas', exist_ok=True)
os.makedirs(f'{base}/api', exist_ok=True)

open(f'{base}/core/__init__.py', 'w').close()
open(f'{base}/models/__init__.py', 'w').close()
open(f'{base}/schemas/__init__.py', 'w').close()
open(f'{base}/api/__init__.py', 'w').close()

with open(f'{base}/requirements.txt', 'w') as f:
    f.write('fastapi\nuvicorn\nsqlalchemy[asyncio]\nasyncpg\npydantic\npydantic-settings\npython-dotenv\ngreenlet\n')

with open(f'{base}/core/database.py', 'w') as f:
    f.write('''import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_accounting")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
''')

with open(f'{base}/models/accounting.py', 'w') as f:
    f.write('''from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
import enum

class AccountType(enum.Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    
    journal_items = relationship("JournalItem", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    journal_entry = relationship("JournalEntry", back_populates="transaction", uselist=False)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)
    
    transaction = relationship("Transaction", back_populates="journal_entry")
    items = relationship("JournalItem", back_populates="journal_entry")

class JournalItem(Base):
    __tablename__ = "journal_items"
    
    id = Column(Integer, primary_key=True, index=True)
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    
    journal_entry = relationship("JournalEntry", back_populates="items")
    account = relationship("Account", back_populates="journal_items")
''')

with open(f'{base}/schemas/transaction.py', 'w') as f:
    f.write('''from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    description: str
    amount: float = Field(..., gt=0, description="Amount must be a positive float")
    transaction_type: str
    
    @field_validator("transaction_type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("Income", "Expense"):
            raise ValueError('transaction_type must be either "Income" or "Expense"')
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
''')

with open(f'{base}/api/transactions.py', 'w') as f:
    f.write('''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.schemas.transaction import TransactionCreate, TransactionResponse
from backend.models.accounting import Transaction

router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    new_transaction = Transaction(
        description=transaction.description,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction
''')

with open(f'{base}/main.py', 'w') as f:
    f.write('''from fastapi import FastAPI
from backend.api import transactions
from backend.core.database import engine, Base
from backend.models import accounting  # ensure models are loaded

app = FastAPI(title="AI-Powered Accounting & Finance Assistant")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables (only for development/demonstration)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(transactions.router, prefix="/api/v1", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Accounting & Finance Assistant API"}
''')
