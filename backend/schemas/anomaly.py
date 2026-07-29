from pydantic import BaseModel
from typing import List

class AnomalyDetail(BaseModel):
    transaction_id: int
    description: str
    amount: float
    reason: str

class AnomalyReport(BaseModel):
    month: int
    year: int
    total_transactions_scanned: int
    anomalies_found: int
    anomalies: List[AnomalyDetail]
