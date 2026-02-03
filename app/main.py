from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="RiskIQ Backend")

app.include_router(router)