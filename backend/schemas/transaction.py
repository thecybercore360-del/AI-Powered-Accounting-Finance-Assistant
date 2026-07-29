from pydantic import BaseModel, Field, field_validator
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
