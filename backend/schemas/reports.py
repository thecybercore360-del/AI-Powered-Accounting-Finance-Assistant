from pydantic import BaseModel

class ProfitAndLossReport(BaseModel):
    total_revenue: float
    total_expenses: float
    net_profit: float

class BalanceSheetReport(BaseModel):
    total_assets: float
    total_liabilities: float
    total_equity: float
    is_balanced: bool
