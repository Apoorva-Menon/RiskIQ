from fastapi import APIRouter
from app.api.schemas import PortfolioUploadRequest, RiskIQResponse
from app.graph.graph import run_graph
from app.graph.state import (
    RiskIQState,
    UserProfile,
    PortfolioInput,
    HoldingInput
)
from fastapi import HTTPException
from pydantic import ValidationError

router = APIRouter()

@router.post("/analyze", response_model=RiskIQResponse)
def analyze_portfolio(request: PortfolioUploadRequest):
    try:
        state = RiskIQState(
            user_profile = UserProfile(
                user_id = request.user_id,
                risk_tolerance = request.risk_tolerance,
                investment_horizon_years = request.investment_horizon_years,
                preferred_sectors = request.preferred_sectors,
            ),
            portfolio_input=PortfolioInput(holdings = [
                HoldingInput(ticker=h.ticker, quantity=h.quantity) for h in request.holdings
            ])
        )

        final_state = run_graph(state)
        report = final_state.report
        return RiskIQResponse(
            risk_score=report.risk_score,
            summary=report.summary,
            detailed_explanation=report.detailed_explanation,
            actionable_suggestions=report.actionable_suggestions,
            confidence_summary=report.confidence_summary
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())