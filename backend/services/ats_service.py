"""
ATS Scoring Service — uses SentenceTransformers for semantic similarity scoring.
Computes cosine similarity between a resume and a job description.
Also extracts keyword matches/gaps using TF-IDF-like token comparison.
"""
import re
from typing import List, Tuple
import numpy as np

# Lazy-load the model to avoid slow startup when the module is first imported
_st_model = None


def _get_model():
    """Lazy-load sentence-transformers model the first time it is needed."""
    global _st_model
    if _st_model is None:
        from sentence_transformers import SentenceTransformer
        _st_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _st_model


def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two numpy vectors."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))


def _extract_keywords(text: str) -> List[str]:
    """
    Simple keyword extractor — lowercases, removes stop words,
    returns unique meaningful tokens (length >= 3).
    """
    stop_words = {
        "and", "the", "for", "with", "you", "are", "our", "will", "have",
        "that", "this", "from", "your", "not", "but", "also", "must", "can",
        "use", "well", "all", "any", "its", "has", "was", "been", "able",
        "work", "work", "team", "role", "based", "using", "strong", "good",
        "etc", "new", "job", "who", "more", "than","responsible"
    }
    tokens = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', text.lower())
    keywords = [t for t in tokens if len(t) >= 3 and t not in stop_words]
    return list(set(keywords))


def calculate_ats_score(
    resume_text: str,
    job_description: str
) -> Tuple[int, List[str], List[str], List[str]]:
    """
    Compute ATS match score using:
    1. Semantic similarity via SentenceTransformers (weighted 60%)
    2. Keyword overlap ratio (weighted 40%)

    Args:
        resume_text: Full text of the resume
        job_description: Full text of the job description

    Returns:
        Tuple of (score 0-100, matching_keywords, missing_keywords, suggestions)
    """
    model = _get_model()

    # ── Semantic Similarity (60% weight) ──────────────────────────────────────
    embeddings = model.encode([resume_text, job_description])
    semantic_sim = _cosine_similarity(embeddings[0], embeddings[1])
    semantic_score = semantic_sim * 100  # normalize to 0-100

    # ── Keyword Overlap (40% weight) ─────────────────────────────────────────
    jd_keywords = set(_extract_keywords(job_description))
    resume_keywords = set(_extract_keywords(resume_text))

    matching = list(jd_keywords & resume_keywords)
    missing = list(jd_keywords - resume_keywords)

    keyword_score = (len(matching) / len(jd_keywords) * 100) if jd_keywords else 0

    # ── Combined Score ────────────────────────────────────────────────────────
    combined_score = int(0.6 * semantic_score + 0.4 * keyword_score)
    combined_score = max(0, min(100, combined_score))  # clamp to 0-100

    # ── Improvement Suggestions ───────────────────────────────────────────────
    suggestions = _generate_suggestions(combined_score, missing, matching)

    # Return top 20 keywords only to keep response clean
    return combined_score, sorted(matching)[:20], sorted(missing)[:20], suggestions


def _generate_suggestions(
    score: int,
    missing: List[str],
    matching: List[str]
) -> List[str]:
    """Generate actionable improvement suggestions based on ATS analysis."""
    suggestions = []

    if score < 40:
        suggestions.append("Your resume needs significant optimization. Consider rewriting it targeting this specific role.")
    elif score < 60:
        suggestions.append("Your resume partially matches the job. Add more job-specific keywords.")
    elif score < 80:
        suggestions.append("Good match! Fine-tune by incorporating a few more key terms from the JD.")
    else:
        suggestions.append("Excellent match! Your resume is well-optimized for this role.")

    if missing:
        top_missing = missing[:8]
        suggestions.append(f"Add these missing keywords: {', '.join(top_missing)}")

    if len(matching) < 10:
        suggestions.append("Use more industry-specific technical terms and action verbs.")

    suggestions.append("Quantify your achievements with numbers (%, $, time saved, team size).")
    suggestions.append("Ensure your skills section explicitly lists the required technologies.")

    return suggestions
