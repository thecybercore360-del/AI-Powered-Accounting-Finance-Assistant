import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

system_prompt = """You are an expert AI-Powered Accounting Auditor. 
Your task is to review a list of transactions for a specific month and identify any anomalies.
Look for two types of anomalies:
1. Duplicate entries (same amount and description on the same or consecutive days).
2. Unusual spikes or exceptionally large amounts that differ wildly from typical transactions.

You will receive a JSON list of transactions.
You MUST output your findings strictly as a JSON array of objects, with each object having the following keys:
- "transaction_id" (integer)
- "description" (string)
- "amount" (float)
- "reason" (string explaining why it is an anomaly)

If no anomalies are found, return an empty array [].
Do NOT include any markdown formatting (like ```json), just the raw JSON text.
"""

async def detect_anomalies_with_ai(transactions_data: list):
    llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY", ""))
    
    # Convert transactions to simple dicts for the prompt
    tx_list = [
        {
            "id": tx.id,
            "description": tx.description,
            "amount": tx.amount,
            "date": tx.created_at.isoformat() if tx.created_at else None
        }
        for tx in transactions_data
    ]
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=json.dumps(tx_list))
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        # Parse the raw JSON string
        result_str = response.content.strip()
        if result_str.startswith("```json"):
            result_str = result_str[7:]
        if result_str.endswith("```"):
            result_str = result_str[:-3]
            
        anomalies = json.loads(result_str.strip())
        return anomalies
    except Exception as e:
        # Fallback if parsing fails
        print(f"Failed to parse AI response: {e}")
        return []
