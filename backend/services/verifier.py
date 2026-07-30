import json

import requests
from requests.exceptions import RequestException


def verify_claim(claim: str) -> dict[str, str]:
    """Verify a claim with Ollama and return status and explanation."""
    if not claim or not claim.strip():
        return {
            "status": "Unknown",
            "explanation": "Empty claim received",
        }

    prompt = f"""
You are a strict fact-checking API.

Respond ONLY with valid JSON.

{{"status": "True", "explanation": "short explanation"}}

Claim: {claim}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=12,
        )
        response.raise_for_status()
    except RequestException:
        return {
            "status": "Unknown",
            "explanation": "Failed to reach Ollama for claim verification.",
        }

    try:
        response_json = response.json()
    except ValueError:
        return {
            "status": "Unknown",
            "explanation": "Ollama returned invalid JSON.",
        }

    output = response_json.get("response")
    if not isinstance(output, str):
        return {
            "status": "Unknown",
            "explanation": "Ollama did not return a valid response field.",
        }

    cleaned_output = output.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned_output)
    except json.JSONDecodeError:
        last_line = cleaned_output.splitlines()[-1].strip()
        try:
            parsed = json.loads(last_line)
        except json.JSONDecodeError:
            return {
                "status": "Unknown",
                "explanation": "Unable to parse Ollama response into JSON.",
            }

    if not isinstance(parsed, dict):
        return {
            "status": "Unknown",
            "explanation": "Ollama response is not a valid JSON object.",
        }

    status = parsed.get("status", "Unknown")
    explanation = parsed.get("explanation", "The claim could not be verified reliably.")
    if status not in {"True", "False", "Unknown"}:
        status = "Unknown"

    return {
        "status": status,
        "explanation": str(explanation),
    }
