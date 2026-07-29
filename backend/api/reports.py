from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.reports import ProfitAndLossReport, BalanceSheetReport
from crud.reports import generate_pl_statement, generate_balance_sheet

router = APIRouter()

@router.get("/reports/pl", response_model=ProfitAndLossReport)
async def get_pl_statement(db: AsyncSession = Depends(get_db)):
    try:
        data = await generate_pl_statement(db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/balance-sheet", response_model=BalanceSheetReport)
async def get_balance_sheet(db: AsyncSession = Depends(get_db)):
    try:
        data = await generate_balance_sheet(db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
