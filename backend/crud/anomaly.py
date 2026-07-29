from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract
from models.accounting import Transaction

async def get_transactions_by_month(db: AsyncSession, month: int, year: int):
    # Fetch all transactions matching the month and year
    query = select(Transaction).filter(
        extract('month', Transaction.created_at) == month,
        extract('year', Transaction.created_at) == year
    )
    result = await db.execute(query)
    transactions = result.scalars().all()
    return transactions
