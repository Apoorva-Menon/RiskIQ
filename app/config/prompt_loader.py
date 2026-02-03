import yaml 
from pathlib import Path

def load_prompt(path: str) -> dict:
    prompt_path = Path(path)
    with open(prompt_path, "r") as f:
        return yaml.safe_load(f)