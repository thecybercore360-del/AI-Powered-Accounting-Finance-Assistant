import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from agent.tools import record_transaction_tool
from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# System prompt to guide the AI
system_prompt = """You are an expert AI-Powered Accounting & Finance Assistant.
Your job is to parse natural language descriptions of financial transactions and record them into the accounting system using the record_transaction_tool.
You must extract the amount, description, transaction_type (Income or Expense), and identify the correct debit and credit accounts.
For now, assume:
- Cash/Bank Account ID = 1
- Rent Expense Account ID = 2
- Sales Revenue Account ID = 3
- Internet Expense Account ID = 4

If a user says "Paid 5000 Rs for office rent", it is an Expense. Debit the Rent Expense Account (2) and Credit Cash (1).
If a user says "Received 10000 Rs for consulting", it is Income. Debit Cash (1) and Credit Sales Revenue (3).

Always reply back to the user with a friendly summary of what was recorded after you execute the tool.
"""

# Initialize LLM and bind tool
llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY", ""))
tools = [record_transaction_tool]
llm_with_tools = llm.bind_tools(tools)

# Define nodes
async def call_model(state: AgentState):
    messages = state["messages"]
    # Ensure system prompt is first
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt)] + list(messages)
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is a tool call, route to tools
    if last_message.tool_calls:
        return "tools"
    return END

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

# Compile graph
app = workflow.compile()
