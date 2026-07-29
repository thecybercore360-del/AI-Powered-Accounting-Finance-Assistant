from langchain_core.tools import tool
from schemas.transaction import TransactionCreate
from crud.accounting import create_double_entry_transaction
from core.database import async_session

@tool("record_transaction_tool")
async def record_transaction_tool(amount: float, description: str, transaction_type: str, debit_account_id: int, credit_account_id: int) -> str:
    """
    Records a new double-entry accounting transaction.
    
    Args:
        amount: The monetary amount of the transaction. Must be positive.
        description: A natural language description of the transaction.
        transaction_type: Either "Income" or "Expense".
        debit_account_id: The ID of the account to be debited. (e.g. 1 for Cash, 2 for Rent)
        credit_account_id: The ID of the account to be credited.
    """
    try:
        # Validate using Pydantic
        tx_data = TransactionCreate(
            amount=amount,
            description=description,
            transaction_type=transaction_type
        )
        
        # Create a new session for this tool execution
        async with async_session() as db:
            result = await create_double_entry_transaction(
                db=db,
                transaction_data=tx_data,
                debit_account_id=debit_account_id,
                credit_account_id=credit_account_id
            )
            return f"Success: Transaction recorded with ID {result.id}"
    except Exception as e:
        return f"Error recording transaction: {str(e)}"
