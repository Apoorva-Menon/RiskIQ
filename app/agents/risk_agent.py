from app.graph.state import (
    RiskIQState,
    RiskState,
    RiskSignals,
    RiskLabels
)

def label_volatility(vol: float) -> str:
    if vol <= 0.18:
        return "low"
    elif vol <= 0.25:
        return "medium"
    else:
        return "high"


def label_hhi(hhi: float) -> str:
    if hhi < 0.15:
        return "low"
    elif hhi <= 0.30:
        return "medium"
    else:
        return "high"


def label_drawdown(dd: float) -> str:
    # dd is negative (e.g., -0.30)
    if dd >= -0.20:
        return "low"
    elif dd >= -0.35:
        return "medium"
    else:
        return "high"


def expected_market_risk_by_tolerance(tolerance: str) -> str:
    return {
        "conservative": "low",
        "moderate": "medium",
        "aggressive": "high",
    }[tolerance]


# -----------------------------
# Main Risk Agent
# -----------------------------

def run_risk_agent(state: RiskIQState) -> RiskIQState:
    analytics = state.analytics
    weights = state.market_data.normalized_holdings
    tolerance = state.user_profile.risk_tolerance

    # -----------------------------
    # Market risk (volatility)
    # -----------------------------
    volatilities = [m.volatility for m in analytics.asset_metrics.values()]
    max_volatility = max(volatilities)
    avg_volatility = sum(volatilities) / len(volatilities)

    market_risk_label = label_volatility(max_volatility)

    # -----------------------------
    # Concentration risk (HHI)
    # -----------------------------
    hhi = sum(w ** 2 for w in weights.values())
    concentration_risk_label = label_hhi(hhi)

    # -----------------------------
    # Drawdown risk
    # -----------------------------
    worst_drawdown = min(
        m.max_drawdown for m in analytics.asset_metrics.values()
    )
    drawdown_risk_label = label_drawdown(worst_drawdown)

    # -----------------------------
    # Risk tolerance alignment
    # -----------------------------
    expected_market_risk = expected_market_risk_by_tolerance(tolerance)
    tolerance_misaligned = (
        market_risk_label == "high" and expected_market_risk != "high"
    )

    # -----------------------------
    # Dominant risk drivers
    # -----------------------------
    drivers = []

    if market_risk_label == "high":
        drivers.append("High volatility assets dominate the portfolio")

    if concentration_risk_label in ("medium", "high"):
        drivers.append("Portfolio is concentrated across a few positions")

    if drawdown_risk_label in ("medium", "high"):
        drivers.append("Potential drawdowns are significant during market stress")

    if tolerance_misaligned:
        drivers.append(
            "Observed risk exceeds the user’s stated risk tolerance"
        )

    if not drivers:
        drivers.append("Portfolio risk is broadly aligned with profile")

    # -----------------------------
    # Populate state
    # -----------------------------
    state.risk = RiskState(
        signals=RiskSignals(
            portfolio_beta=1.0 + (avg_volatility - 0.20),  # synthetic, stable
            concentration_hhi=round(hhi, 4),
            value_at_risk_95=round(worst_drawdown * 0.6, 4),  # synthetic proxy
        ),
        labels=RiskLabels(
            market_risk=market_risk_label,
            concentration_risk=concentration_risk_label,
            drawdown_risk=drawdown_risk_label,
        ),
        dominant_risk_drivers=drivers,
    )

    return state