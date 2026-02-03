import json
import re
from typing import Any

class LLMResponseJSONParseError:
    pass

def parse_llm_response_json(raw_text: str) -> Any:
    """
    Extracts and parses a JSON object from LLM response.
    Handles markdown fences and stray text safely.
    """
    if not raw_text or not raw_text.strip():
        raise LLMResponseJSONParseError("Empty response from LLM")
    
    text = raw_text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            pass

    raise LLMResponseJSONParseError("No valid JSON object found in LLM output")