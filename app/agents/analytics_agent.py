from app.graph.state import (
    RiskIQState,
    AnalyticsState,
    AnalyticsMetrics
)
import math
import random

def run_analytics_agent(state: RiskIQState) -> RiskIQState:
    """
    Analytics Agent
    -----------------------
    - Uses deterministic, synthetic metrics.
    """

    normalized_holdings = state.market_data.normalized_holdings

    if not normalized_holdings:
        raise ValueError("AnalyticsAgent: normalized_holdings missing or empty")

    asset_metrics = {}

    seed = hash(tuple(sorted(normalized_holdings.items())))
    rng = random.Random(seed)

    for ticker, weight in normalized_holdings.items():
        mean_return = 0.05 + (0.05 * weight)
        volatility = 0.15 + (0.15 * weight)
        sharpe_ratio = round(mean_return / volatility, 2)
        max_drawdown = -0.2 - (0.2 * weight)

        asset_metrics[ticker] = AnalyticsMetrics(
            mean_return= round(mean_return, 4),
            volatility= round(volatility, 4),
            sharpe_ratio=sharpe_ratio,
            max_drawdown= round(max_drawdown, 4)
        )

    portfolio_return_series=[]
    base_return = sum(
        asset.mean_return * normalized_holdings[ticker]
        for ticker, asset in asset_metrics.items()
    )

    for i in range(10):
        fluctuation = math.sin(i) * 0.01
        portfolio_return_series.append(round(base_return + fluctuation, 4))

    # Correlation matrix (identity-like for Phase 1)
    correlation_matrix = {
        t1: {t2: (1.0 if t1 == t2 else 0.3) for t2 in asset_metrics}
        for t1 in asset_metrics
    }

    state.analytics = AnalyticsState(
        asset_metrics=asset_metrics,
        portfolio_return_series=portfolio_return_series,
        correlation_matrix=correlation_matrix
    )

    return state