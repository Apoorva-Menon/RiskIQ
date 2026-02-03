from app.graph.state import RiskIQState
from app.agents.data_agent import run_data_agent
from app.agents.analytics_agent import run_analytics_agent
from app.agents.risk_agent import run_risk_agent
from app.agents.reporting_agent import run_reporting_agent

def data_node(state: RiskIQState) -> RiskIQState:
    return run_data_agent(state)


def analytics_node(state: RiskIQState) -> RiskIQState:
    return run_analytics_agent(state)


def risk_node(state: RiskIQState) -> RiskIQState:
    return run_risk_agent(state)


def reporting_node(state: RiskIQState) -> RiskIQState:
    return run_reporting_agent(state)
