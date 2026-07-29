from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import transactions
from api import chat
from api import reports
from api import anomaly
from core.database import engine, Base
from models import accounting  # ensure models are loaded

app = FastAPI(title="AI-Powered Accounting & Finance Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables (only for development/demonstration)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(transactions.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(chat.router, prefix="/api/v1", tags=["AI Chat"])
app.include_router(reports.router, prefix="/api/v1", tags=["Financial Reports"])
app.include_router(anomaly.router, prefix="/api/v1", tags=["AI Audit"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Accounting & Finance Assistant API"}
