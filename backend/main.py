from fastapi import FastAPI
from api import transactions
from api import chat
from core.database import engine, Base
from models import accounting  # ensure models are loaded

app = FastAPI(title="AI-Powered Accounting & Finance Assistant")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables (only for development/demonstration)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(transactions.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(chat.router, prefix="/api/v1", tags=["AI Chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Accounting & Finance Assistant API"}
