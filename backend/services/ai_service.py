"""
AI Service — wraps the Google Gemini API for all LLM-powered generation tasks.
Uses the new `google-genai` SDK (v1.x) with automatic retry on rate limits.
"""
import time
import logging
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts.resume_prompt import build_resume_prompt
from prompts.cover_letter_prompt import build_cover_letter_prompt
from prompts.portfolio_prompt import build_portfolio_prompt

logger = logging.getLogger(__name__)

# Create a single client instance (thread-safe, reusable)
_client = genai.Client(api_key=GEMINI_API_KEY)


def _call_gemini(prompt: str, max_retries: int = 3) -> str:
    """
    Send a prompt to Gemini and return the text response.
    Automatically retries on 429 rate-limit errors with exponential backoff.
    Raises RuntimeError on unrecoverable failure.
    """
    for attempt in range(max_retries):
        try:
            response = _client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=8192,
                ),
            )
            return response.text.strip()

        except ClientError as e:
            error_str = str(e)
            # 429 RESOURCE_EXHAUSTED — rate limited, wait and retry
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait = (attempt + 1) * 15  # 15s, 30s, 45s
                logger.warning(f"Gemini rate limited (attempt {attempt+1}/{max_retries}). Waiting {wait}s...")
                if attempt < max_retries - 1:
                    time.sleep(wait)
                    continue
                raise RuntimeError(
                    "Gemini API rate limit exceeded. Please wait a moment and try again. "
                    "Consider upgrading your API plan for higher quotas."
                )
            # 400 INVALID_ARGUMENT — usually wrong model name
            elif "400" in error_str or "INVALID_ARGUMENT" in error_str:
                raise RuntimeError(
                    f"Gemini API invalid request. Check your GEMINI_MODEL in .env. Error: {error_str}"
                )
            # 401/403 — API key issue
            elif "401" in error_str or "403" in error_str or "API_KEY" in error_str:
                raise RuntimeError(
                    "Gemini API key is invalid or missing. Check GEMINI_API_KEY in your .env file."
                )
            else:
                raise RuntimeError(f"Gemini API error: {error_str}")

        except Exception as e:
            raise RuntimeError(f"Gemini API unexpected error: {str(e)}")

    raise RuntimeError("Gemini API failed after all retries.")


# ─── Resume Generation ────────────────────────────────────────────────────────

def generate_resume(profile: dict, job_role: str, job_description: str = "") -> str:
    """Generate an ATS-optimized resume in Markdown format."""
    prompt = build_resume_prompt(profile, job_role, job_description)
    return _call_gemini(prompt)


# ─── Cover Letter Generation ──────────────────────────────────────────────────

def generate_cover_letter(
    profile: dict,
    company_name: str,
    job_role: str,
    job_description: str,
    hiring_manager: str = "Hiring Manager"
) -> str:
    """Generate a tailored cover letter for a specific company and role."""
    prompt = build_cover_letter_prompt(
        profile, company_name, job_role, job_description, hiring_manager
    )
    return _call_gemini(prompt)


# ─── Portfolio Generation ─────────────────────────────────────────────────────

def generate_portfolio(profile: dict) -> dict:
    """Generate all portfolio content sections from the user's profile."""
    prompt = build_portfolio_prompt(profile)
    raw = _call_gemini(prompt)
    return _parse_portfolio_sections(raw)


def _parse_portfolio_sections(raw_text: str) -> dict:
    """
    Parse Gemini's portfolio output into structured sections.
    Expects labels like: [ABOUT_ME], [BIO], [LINKEDIN], [PROJECT:name], [GITHUB]
    """
    result = {
        "about_me": "",
        "professional_bio": "",
        "linkedin_summary": "",
        "project_descriptions": [],
        "github_highlights": ""
    }

    current_key = None
    current_content = []

    for line in raw_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[ABOUT_ME]"):
            current_key = "about_me"; current_content = []
        elif stripped.startswith("[BIO]"):
            if current_key: result = _flush(result, current_key, current_content)
            current_key = "professional_bio"; current_content = []
        elif stripped.startswith("[LINKEDIN]"):
            if current_key: result = _flush(result, current_key, current_content)
            current_key = "linkedin_summary"; current_content = []
        elif stripped.startswith("[PROJECT:"):
            if current_key: result = _flush(result, current_key, current_content)
            project_name = stripped[9:].rstrip("]")
            current_key = f"project:{project_name}"; current_content = []
        elif stripped.startswith("[GITHUB]"):
            if current_key: result = _flush(result, current_key, current_content)
            current_key = "github_highlights"; current_content = []
        else:
            if current_key:
                current_content.append(line)

    if current_key:
        result = _flush(result, current_key, current_content)

    return result


def _flush(result: dict, key: str, content: list) -> dict:
    """Helper to assign accumulated content to the appropriate result key."""
    text = "\n".join(content).strip()
    if key.startswith("project:"):
        result["project_descriptions"].append({"name": key[8:], "description": text})
    elif key in result:
        result[key] = text
    return result
