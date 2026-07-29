from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.accounting import Transaction, JournalEntry, JournalItem, Account
from schemas.transaction import TransactionCreate

async def create_double_entry_transaction(db: AsyncSession, transaction_data: TransactionCreate, debit_account_id: int, credit_account_id: int):
    # 1. Create the main Transaction record
    new_transaction = Transaction(
        description=transaction_data.description,
        amount=transaction_data.amount,
        transaction_type=transaction_data.transaction_type
    )
    db.add(new_transaction)
    await db.flush()  # Flush to get the transaction ID

    # 2. Create the associated Journal Entry
    journal_entry = JournalEntry(
        transaction_id=new_transaction.id,
        description=f"Journal Entry for: {transaction_data.description}"
    )
    db.add(journal_entry)
    await db.flush()

    # 3. Create the Debit Journal Item
    debit_item = JournalItem(
        journal_entry_id=journal_entry.id,
        account_id=debit_account_id,
        debit=transaction_data.amount,
        credit=0.0
    )
    db.add(debit_item)

    # 4. Create the Credit Journal Item
    credit_item = JournalItem(
        journal_entry_id=journal_entry.id,
        account_id=credit_account_id,
        debit=0.0,
        credit=transaction_data.amount
    )
    db.add(credit_item)

    # 5. Validation Check: SUM(Debits) == SUM(Credits)
    if debit_item.debit != credit_item.credit:
        raise HTTPException(status_code=400, detail="Double-Entry Validation Failed: Debits do not equal Credits.")

    # 6. Commit all changes atomically
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction
