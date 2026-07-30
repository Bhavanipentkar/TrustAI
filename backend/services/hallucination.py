def detect_hallucination(status: str) -> str:
    """Map a claim verification status to a hallucination risk level."""
    if status == "True":
        return "Low"
    if status == "False":
        return "Medium"
    return "High"
