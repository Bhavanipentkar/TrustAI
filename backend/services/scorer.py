def generate_score(results):
    """Generate an overall trust score and verdict from verification results."""
    score = 50

    for result in results:
        status = result.get("status", "Unknown")
        if status == "True":
            score += 20
        elif status == "False":
            score -= 20
        else:
            score += 5

    score = max(0, min(100, score))

    if score >= 80:
        verdict = "Reliable"
    elif score >= 45:
        verdict = "Uncertain"
    else:
        verdict = "Unreliable"

    return {
        "trust_score": score,
        "verdict": verdict,
    }
