##RiskIQ: Intelligent Portfolio Evaluation System

RiskIQ is a multi-agent system for analyzing and explaining the **risk characteristics of an equity portfolio**.
It combines **deterministic financial analytics** with **LLM-based professional reporting**, orchestrated using **LangGraph**.

##Problem Statement:

Most portfolio risk tools either:
- expose raw metrics without interpretation, or
- provide black-box recommendations without transparency.

**RiskIQ bridges this gap** by:
- computing interpretable risk metrics deterministically,
- separating analytics, risk assessment, and reporting into distinct agents,
- producing professional, compliance-safe explanations of portfolio risk.

## Architecture Overview

RiskIQ uses a **mutli-agent** pipeline, orchestrated via LangGraph:

Input (JSON)
↓
Data Agent
↓
Analytics Agent
↓
Risk Agent
↓
Reporting Agent (LLM-powered)
↓
Structured Risk Report (JSON)


### Agents

#### Data Agent
- Validates and normalizes portfolio holdings
- Prepares market data inputs

#### Analytics Agent
Computes portfolio-level metrics such as:
- normalized weights,
- volatility,
- beta,
- concentration (HHI),
- Value-at-Risk (VaR).

#### Risk Agent
- Applies deterministic heuristics to classify:
  - market risk,
  - concentration risk,
  - drawdown risk.
- Produces risk signals and dominant risk drivers.

#### Reporting Agent
- Uses **Google Gemini (via LangChain)** to generate a professional, analyst-style risk report
- Outputs **strictly structured JSON**
- Performs **no calculations or recommendations**

---

## Current Features (Implemented)

- JSON-based portfolio input
- Strict input validation (FastAPI + Pydantic)
- Deterministic analytics and risk classification
- Multi-agent orchestration with LangGraph
- LLM-powered reporting with output sanitization
- Clean **200 / 422 / 500** behavior
- End-to-end `/analyze` API endpoint

---

## How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Set environment variable

export GOOGLE_API_KEY=your_api_key_here

### 3. Start the app

uvicorn app.main:app --reload

## 4. Call the API

POST /analyze with the request (sample request in data/fixtures/sample_portfolio.json)

### 5. Sample Request:

{
  "user_id": "user_001",
  "risk_tolerance": "moderate",
  "investment_horizon_years": 5,
  "preferred_sectors": ["Technology", "Healthcare"],
  "holdings": [
    { "ticker": "APPL", "quantity": 100 },
    { "ticker": "MSFT", "quantity": 1 },
    { "ticker": "NVDA", "quantity": 1 }
  ]
}

### 6. Sample Response:

{
  "risk_score": 100,
  "summary": "The portfolio's current risk profile is assessed as high, which appears to exceed the user's stated moderate risk tolerance. This assessment is primarily driven by a significant concentration in a few positions and a high sensitivity to market volatility. The observed risk characteristics suggest a potential misalignment with the specified investor profile.",
  "detailed_explanation": "The primary sources of risk are high concentration and exposure to market volatility. The concentration risk is labeled as high, with a corresponding HHI score of 0.9614, indicating that the portfolio's value is dominated by a very small number of assets. This lack of diversification can amplify the impact of poor performance from any single holding.\n\nFurthermore, the portfolio's market risk is high, with a beta near 1.0, suggesting it is expected to move in line with the broader market. The combination of high concentration and market sensitivity contributes to a high drawdown risk. The 95% Value-at-Risk of -23.77% indicates a significant potential for loss under adverse market conditions, based on the model's assumptions.",
  "actionable_suggestions": [
    "Review the portfolio's concentration to assess whether broader diversification across a larger number of assets could better align with the stated risk tolerance.",
    "Evaluate the overall volatility of the holdings to determine if a rebalancing towards a mix of assets with different risk characteristics might be appropriate.",
    "Consider the balance of exposures across different economic sectors to mitigate risks associated with any single industry.",
    "Conduct a holistic review of the portfolio's holdings against the investment horizon and moderate risk profile to ensure long-term alignment."
  ],
  "confidence_summary": "This assessment is based on a static analysis of the provided portfolio data and uses simplified risk models. It does not incorporate real-time market data or predict future performance, and the risk metrics represent estimates under specific model assumptions."
}

## Disclaimer

This project is for educational and exploratory purposes only.
It does not provide investment advice, recommendations, or forecasts.