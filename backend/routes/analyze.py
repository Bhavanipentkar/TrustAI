from fastapi import APIRouter
from models.request_model import InputText
from services.claim_extractor import extract_claims
from services.hallucination import detect_hallucination
from services.scorer import generate_score
from services.verifier import verify_claim

router = APIRouter()


def _build_summary(results: list[dict[str, str]], trust_score: int, verdict: str) -> str:
    """Create a beginner-friendly summary for the evaluation output."""
    if not results:
        return "No factual claims were detected. Please provide more detail so TrustAI can analyze the text."

    true_count = sum(1 for item in results if item["status"] == "True")
    false_count = sum(1 for item in results if item["status"] == "False")
    unknown_count = sum(1 for item in results if item["status"] == "Unknown")

    if verdict == "Reliable":
        return (
            f"AI response appears reliable because {true_count} claim(s) were verified as True and the overall trust score is {trust_score}."
        )
    if verdict == "Uncertain":
        return (
            f"AI response appears uncertain because {unknown_count} claim(s) could not be verified clearly, while {true_count} claim(s) appear reliable."
        )

    return (
        f"AI response appears unreliable because {false_count} claim(s) were marked False and the score is {trust_score}."
    )


@router.post("/analyze")
async def analyze(payload: InputText):
    """Analyze incoming text and return structured AI trust results."""
    claims = extract_claims(payload.text)
    print("DEBUG CLAIMS:", claims)
    results = []

    for claim in claims:
        if not claim or not claim.strip():
            continue

        print("DEBUG SENDING CLAIM:", claim)
        verification = verify_claim(claim)
        hallucination = detect_hallucination(verification["status"])
        results.append(
            {
                "claim": claim,
                "status": verification["status"],
                "explanation": verification["explanation"],
                "hallucination": hallucination,
            }
        )

    trust_data = generate_score(results)
    summary = _build_summary(results, trust_data["trust_score"], trust_data["verdict"])

    return {
        "claims": claims,
        "results": results,
        "trust_score": trust_data["trust_score"],
        "verdict": trust_data["verdict"],
        "summary": summary,
    }
