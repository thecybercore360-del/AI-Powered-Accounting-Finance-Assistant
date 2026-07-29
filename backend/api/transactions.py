from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.transaction import TransactionCreate, TransactionResponse
from models.accounting import Transaction

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
