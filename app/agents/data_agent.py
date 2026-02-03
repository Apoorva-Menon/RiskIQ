from app.graph.state import (
    RiskIQState, MarketDataState, DataQualityFlags
)

def run_data_agent(state: RiskIQState) -> RiskIQState:
    holdings = state.portfolio_input.holdings

    invalid_tickers = []
    total_quantity = 0.0

    for h in holdings:
        if not h.ticker or not isinstance(h.ticker, str):
            invalid_tickers.append(h.ticker)
        if h.quantity <= 0:
            raise ValueError(f"Invalid quantity for {h.ticker}")
        total_quantity += h.quantity

    if total_quantity == 0:
        raise ValueError("Total portfolio quantity cannot be zero")

    normalized_holdings = {
        h.ticker.upper(): h.quantity / total_quantity
        for h in holdings
    }

    state.market_data = MarketDataState(
        normalized_holdings=normalized_holdings,
        data_quality=DataQualityFlags(
            invalid_tickers=invalid_tickers,
            missing_price_days={},
            insufficient_history=[]
        )
    )

    return state