"""
Pydantic schemas for resume, cover letter, ATS, and portfolio modules.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ─── Resume ───────────────────────────────────────────────────────────────────

class ResumeGenerateRequest(BaseModel):
    job_role: str
    job_description: Optional[str] = None
    extra_instructions: Optional[str] = None


class ResumeResponse(BaseModel):
    resume_markdown: str
    job_role: str
    history_id: Optional[int] = None


# ─── Cover Letter ─────────────────────────────────────────────────────────────

class CoverLetterRequest(BaseModel):
    company_name: str
    job_role: str
    job_description: str
    hiring_manager: Optional[str] = "Hiring Manager"


class CoverLetterResponse(BaseModel):
    cover_letter: str
    company_name: str
    history_id: Optional[int] = None


# ─── ATS Analyzer ─────────────────────────────────────────────────────────────

class ATSRequest(BaseModel):
    job_description: str
    resume_text: Optional[str] = None   # if None, use user's latest resume


class ATSResponse(BaseModel):
    score: int                          # 0–100
    matching_keywords: List[str]
    missing_keywords: List[str]
    improvement_suggestions: List[str]


# ─── Portfolio ────────────────────────────────────────────────────────────────

class PortfolioResponse(BaseModel):
    about_me: str
    professional_bio: str
    linkedin_summary: str
    project_descriptions: List[dict]
    github_highlights: str
    history_id: Optional[int] = None


# ─── History ─────────────────────────────────────────────────────────────────

class HistoryItem(BaseModel):
    id: int
    job_role: Optional[str]
    company_name: Optional[str]
    generation_type: str
    ats_score: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
