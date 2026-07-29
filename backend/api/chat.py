from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent.graph import app as agent_app

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        inputs = {"messages": [HumanMessage(content=request.message)]}
        # Run the agent workflow
        final_state = await agent_app.ainvoke(inputs)
        
        # The final reply from the AI is the last message content
        final_message = final_state["messages"][-1]
        
        return ChatResponse(reply=final_message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
