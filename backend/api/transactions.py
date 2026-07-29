from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.transaction import TransactionCreate, TransactionResponse
from models.accounting import Transaction
from crud.accounting import create_double_entry_transaction

router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    # TODO: In Step 3, the AI Agent will dynamically determine debit/credit accounts
    # For now, we are hardcoding dummy account IDs (1 and 2) to test the Double-Entry Logic
    try:
        new_transaction = await create_double_entry_transaction(
            db=db, 
            transaction_data=transaction, 
            debit_account_id=1,   # Dummy Account ID
            credit_account_id=2   # Dummy Account ID
        )
        return new_transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
