from pydantic import BaseModel
from typing import Optional, List

class HoldingRequest(BaseModel):
    ticker: str
    quantity: float

class PortfolioUploadRequest(BaseModel):
    user_id: str
    risk_tolerance: str
    investment_horizon_years: Optional[int] = None
    holdings: List[HoldingRequest]
    preferred_sectors: Optional[List[str]] = None

class RiskIQResponse(BaseModel):
    risk_score: int
    summary: str
    detailed_explanation: str
    actionable_suggestions: List[str]
    confidence_summary: str