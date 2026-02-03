from app.graph.state import RiskIQState, ReportState
from app.config.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config.llm_response_json_parser import parse_llm_response_json
import json
import os
import yaml

def compute_risk_score(state: RiskIQState) -> int:
    score = 0

    market = state.risk.labels.market_risk
    concentration = state.risk.labels.concentration_risk
    drawdown = state.risk.labels.drawdown_risk

    score += {"low": 10, "medium": 25, "high": 40}.get(market, 0)
    score += {"low": 10, "medium": 20, "high": 30}.get(concentration, 0)
    score += {"low": 10, "medium": 20, "high": 30}.get(drawdown, 0)

    if "exceeds the user's stated risk tolerance" in " ".join(state.risk.dominant_risk_drivers):
        score += 10

    return min(score, 100)

def build_structured_input(state: RiskIQState) -> dict:
    return {
        "user_profile": {
            "risk_tolerance": state.user_profile.risk_tolerance,
            "investment_horizon_years": state.user_profile.investment_horizon_years,
            "preferred_sectors": state.user_profile.preferred_sectors,
        },
        "risk_labels": state.risk.labels.model_dump(),
        "risk_signals": state.risk.signals.model_dump(),
        "dominant_risk_drivers": state.risk.dominant_risk_drivers
    }

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.2,
        max_output_tokens=2000,
    )

def run_reporting_agent(state: RiskIQState) -> RiskIQState:
    print("DEBUG REPORTING AGENT START")
    print("GOOGLE_API_KEY present:", bool(os.getenv("GOOGLE_API_KEY")))
    prompt = load_prompt("app/prompts/reporting_prompt.yaml")
    risk_score = compute_risk_score(state)
    structured_input = build_structured_input(state)

    system_message = SystemMessage(
        content="\n\n".join([
            prompt["system_role"],
            prompt["hard_constraints"],
            prompt["input_description"],
            yaml.dump(prompt["output_requirements"], sort_keys=False),
            prompt["style_guidelines"],
            prompt["output_format"],
            prompt["length_constraints"],
        ])
    )
    print("INPUT:", structured_input)
    human_message = HumanMessage(
        content=f"""
        Structured input (JSON):
        {json.dumps(structured_input, indent=2)}

        Generate the report according to the output requirements
        """
    )
    llm = get_llm()

    try:
        response = llm.invoke([system_message, human_message])
        print("RAW GEMINI RESPONSE:", response)
        print("RAW GEMINI CONTENT:", getattr(response, "content", None))

        report_json = parse_llm_response_json(response.content)

        state.report = ReportState(
            risk_score=risk_score,
            summary=report_json["summary"],
            detailed_explanation=report_json["detailed_explanation"],
            actionable_suggestions=report_json["actionable_suggestions"],
            confidence_summary=report_json["confidence_summary"]
        )

    except Exception as e:
        print("REPORTING AGENT EXCEPTION:", repr(e))

        report = ReportState(
            risk_score=risk_score,
            summary="The portfolio exhibits notable risk characteristics based on the current assessmsent.",
            detailed_explanation=(
                "The risk assessment is derived from deterministic analytics and heuristic evaluation. "
                "While the portfolio shows exposure to market, concentration, and drawdown risks, "
                "this summary is generated without natural language synthesis due to a processing fallback."
            ),
            actionable_suggestions=[
                "Review portfolio diversification.",
                "Assess alignment with stated risk tolerance.",
                "Monitor exposure to volatile assets."
            ],
            confidence_summary=(
                "This assessment is based on simplified models and does not incorporate real-time market data."
            ),
        )
        state.report = report
    return state

def reporting_node(state: RiskIQState):
    return run_reporting_agent(state)