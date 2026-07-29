from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.accounting import Account, JournalItem, AccountType

async def generate_pl_statement(db: AsyncSession):
    # Calculate Total Revenue (Credits on Revenue Accounts)
    revenue_query = select(func.coalesce(func.sum(JournalItem.credit) - func.sum(JournalItem.debit), 0)).join(Account).filter(Account.account_type == AccountType.REVENUE)
    result = await db.execute(revenue_query)
    total_revenue = result.scalar() or 0.0

    # Calculate Total Expenses (Debits on Expense Accounts)
    expense_query = select(func.coalesce(func.sum(JournalItem.debit) - func.sum(JournalItem.credit), 0)).join(Account).filter(Account.account_type == AccountType.EXPENSE)
    result = await db.execute(expense_query)
    total_expenses = result.scalar() or 0.0

    net_profit = total_revenue - total_expenses
    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit
    }

async def generate_balance_sheet(db: AsyncSession):
    # Calculate Assets (Debits - Credits)
    asset_query = select(func.coalesce(func.sum(JournalItem.debit) - func.sum(JournalItem.credit), 0)).join(Account).filter(Account.account_type == AccountType.ASSET)
    result = await db.execute(asset_query)
    total_assets = result.scalar() or 0.0

    # Calculate Liabilities (Credits - Debits)
    liability_query = select(func.coalesce(func.sum(JournalItem.credit) - func.sum(JournalItem.debit), 0)).join(Account).filter(Account.account_type == AccountType.LIABILITY)
    result = await db.execute(liability_query)
    total_liabilities = result.scalar() or 0.0

    # Calculate Equity (Credits - Debits) + Net Profit
    equity_query = select(func.coalesce(func.sum(JournalItem.credit) - func.sum(JournalItem.debit), 0)).join(Account).filter(Account.account_type == AccountType.EQUITY)
    result = await db.execute(equity_query)
    base_equity = result.scalar() or 0.0

    # Retained earnings (Net Profit) is added to Equity
    pl_data = await generate_pl_statement(db)
    total_equity = base_equity + pl_data["net_profit"]

    # Balance Sheet Equation: Assets = Liabilities + Equity
    # We use round to handle floating point precision issues
    is_balanced = round(total_assets, 2) == round(total_liabilities + total_equity, 2)

    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "is_balanced": is_balanced
    }
