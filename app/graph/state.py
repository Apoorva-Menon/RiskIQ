from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class UserProfile(BaseModel):
    user_id: str
    risk_tolerance: Literal["conservative", "moderate", "aggressive"]
    investment_horizon_years: Optional[int] = None
    preferred_sectors: Optional[List[str]] = None

class HoldingInput(BaseModel):
    ticker: str
    quantity: float

class PortfolioInput(BaseModel):
    holdings: List[HoldingInput]
    base_currency: str = "USD"

class DataQualityFlags(BaseModel):
    invalid_tickers: List[str] = []
    missing_price_days: Dict[str, int] = {}
    insufficient_history: List[str] = []

class MarketDataMeta(BaseModel):
    data_source: str
    retrieved_at: datetime
    last_market_close: datetime
    freshness_hours: float

class MarketDataState(BaseModel):
    normalized_holdings: Optional[Dict[str, float]] = None
    price_series: Optional[Dict[str, List[float]]] = None
    data_quality: Optional[DataQualityFlags] = None
    metadata: Optional[MarketDataMeta] = None

class AnalyticsMetrics(BaseModel):
    mean_return: float
    volatility: float
    sharpe_ratio: Optional[float]
    max_drawdown: float

class AnalyticsState(BaseModel):
    asset_metrics: Dict[str, AnalyticsMetrics]
    portfolio_return_series: List[float]
    correlation_matrix: Dict[str, Dict[str, float]]
    rolling_volatility: Optional[List[float]] = None

class RiskSignals(BaseModel):
    portfolio_beta: float
    concentration_hhi: float
    value_at_risk_95: float

class RiskLabels(BaseModel):
    market_risk: Literal["low", "medium", "high"]
    concentration_risk: Literal["low", "medium", "high"]
    drawdown_risk: Literal["low", "medium", "high"]

class RiskState(BaseModel):
    signals: RiskSignals
    labels: RiskLabels
    dominant_risk_drivers: List[str]

class ConfidenceFactors(BaseModel):
    data_coverage_pct: float
    freshness_hours: float
    assumption_notes: List[str]
    limitations_notes: List[str]

class EvaluationMetrics(BaseModel):
    execution_time_ms: int
    tool_calls: int
    retries: int
    schema_validation_errors: int
    cross_agent_consistency_passed: bool

class ReportState(BaseModel):
    risk_score: int
    summary: str
    detailed_explanation: str
    actionable_suggestions: List[str]
    confidence_summary: str

class AgentTraceEntry(BaseModel):
    agent_name: str
    started_at: datetime
    ended_at: datetime
    status: Literal["success", "failure"]
    notes: Optional[str] = None

class RiskIQState(BaseModel):

    user_profile: UserProfile
    portfolio_input: PortfolioInput
    market_data: Optional[MarketDataState] = None
    analytics: Optional[AnalyticsState] = None
    risk: Optional[RiskState] = None
    confidence: Optional[ConfidenceFactors] = None
    evaluation: Optional[EvaluationMetrics] = None
    report: Optional[ReportState] = None
    agent_trace: Optional[AgentTraceEntry] = None