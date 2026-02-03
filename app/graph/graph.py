from langgraph.graph import StateGraph, END
from app.graph.state import RiskIQState
from app.graph.nodes import (
    data_node,
    analytics_node,
    risk_node,
    reporting_node
)


def build_graph():
    graph = StateGraph(RiskIQState)

    # Register nodes
    graph.add_node("data", data_node)
    graph.add_node("run_analytics", analytics_node)
    graph.add_node("run_risk", risk_node)
    graph.add_node("run_reporting", reporting_node)

    # Define execution order
    graph.set_entry_point("data")
    graph.add_edge("data", "run_analytics")
    graph.add_edge("run_analytics", "run_risk")
    graph.add_edge("run_risk", "run_reporting")
    graph.add_edge("run_reporting", END)

    return graph.compile()


_graph = build_graph()


def run_graph(state: RiskIQState) -> RiskIQState:
    """
    Entry point used by FastAPI.
    Executes the LangGraph pipeline.
    """
    result = _graph.invoke(state)
    return RiskIQState(**result)
