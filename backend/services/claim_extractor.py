import json
from typing import List

import requests
from requests.exceptions import RequestException

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


def _call_ollama(prompt: str) -> str | None:
    """Call the local Ollama API and return the raw text response."""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt},
            timeout=12,
        )
        response.raise_for_status()
        return response.text
    except RequestException:
        return None


def _parse_json_array(raw_text: str) -> List[str] | None:
    """Parse a JSON array from raw text if possible."""
    if not raw_text:
        return None

    cleaned = raw_text.strip()
    if not cleaned:
        return None

    try:
        payload = json.loads(cleaned)
        if isinstance(payload, list) and all(isinstance(item, str) for item in payload):
            return payload
        if isinstance(payload, dict):
            candidate = payload.get("output") or payload.get("response") or payload.get("text")
            if isinstance(candidate, str):
                try:
                    parsed_candidate = json.loads(candidate)
                    if isinstance(parsed_candidate, list) and all(isinstance(item, str) for item in parsed_candidate):
                        return parsed_candidate
                except json.JSONDecodeError:
                    pass
    except json.JSONDecodeError:
        pass

    # If streaming output or extra text is present, try the last line.
    last_line = cleaned.splitlines()[-1].strip()
    try:
        payload = json.loads(last_line)
        if isinstance(payload, list) and all(isinstance(item, str) for item in payload):
            return payload
        if isinstance(payload, dict):
            candidate = payload.get("output") or payload.get("response") or payload.get("text")
            if isinstance(candidate, str):
                try:
                    parsed_candidate = json.loads(candidate)
                    if isinstance(parsed_candidate, list) and all(isinstance(item, str) for item in parsed_candidate):
                        return parsed_candidate
                except json.JSONDecodeError:
                    pass
    except json.JSONDecodeError:
        return None

    return None


def extract_claims(text: str) -> List[str]:
    """Extract factual claims from text.

    This function returns a clean list of claims by splitting text on periods,
    removing whitespace, and ignoring empty or very short sentences.
    """
    if not text or not isinstance(text, str):
        return []

    prompt = (
        "Extract factual claims from the following text. Return ONLY a JSON array.\n\n"
        f"Text: {text}"
    )

    raw_response = _call_ollama(prompt)
    claims = _parse_json_array(raw_response) if raw_response else None

    if claims:
        cleaned_claims = [claim.strip() for claim in claims if isinstance(claim, str) and len(claim.strip()) >= 5]
        if cleaned_claims:
            return cleaned_claims

    # Fallback: split on periods and keep only sentences with enough content.
    sentences = [segment.strip() for segment in text.split(".")]
    return [sentence for sentence in sentences if len(sentence) >= 5]
