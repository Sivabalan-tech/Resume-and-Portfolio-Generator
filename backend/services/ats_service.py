"""
ATS Scoring Service — uses Gemini (via ai_service) for semantic similarity scoring.
This avoids high memory usage of local models like SentenceTransformers on Render.
"""
from typing import List, Tuple
from services.ai_service import analyze_ats

def calculate_ats_score(
    resume_text: str,
    job_description: str
) -> Tuple[int, List[str], List[str], List[str]]:
    """
    Compute ATS match score using Gemini.
    
    Returns:
        Tuple of (score 0-100, matching_keywords, missing_keywords, suggestions)
    """
    # Simply delegate to the AI service which now handles the semantic logic
    return analyze_ats(resume_text, job_description)
