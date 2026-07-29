from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.anomaly import AnomalyReport, AnomalyDetail
from crud.anomaly import get_transactions_by_month
from agent.anomaly import detect_anomalies_with_ai

router = APIRouter()

@router.get("/audit/anomalies", response_model=AnomalyReport)
async def audit_monthly_anomalies(
    month: int,
    year: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        # 1. Fetch transactions for the month
        transactions = await get_transactions_by_month(db, month, year)
        
        # 2. Run AI Analysis
        anomalies_data = await detect_anomalies_with_ai(transactions)
        
        # 3. Format response
        anomalies = [AnomalyDetail(**item) for item in anomalies_data]
        
        return AnomalyReport(
            month=month,
            year=year,
            total_transactions_scanned=len(transactions),
            anomalies_found=len(anomalies),
            anomalies=anomalies
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
