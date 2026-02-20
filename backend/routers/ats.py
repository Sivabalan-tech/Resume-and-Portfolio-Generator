"""
ATS Router — analyzes job descriptions and scores resume-JD match.
Endpoints:
  POST /api/ats/analyze   — compute ATS score for user's resume vs JD
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.profile import Profile
from models.resume_history import ResumeHistory
from schemas.resume import ATSRequest, ATSResponse
from services.auth_service import get_current_user
from services.ats_service import calculate_ats_score
import json

router = APIRouter(prefix="/api/ats", tags=["ATS Analyzer"])


def _profile_to_text(profile: Profile) -> str:
    """Convert profile JSON to a plain-text representation for ATS scoring."""
    parts = []

    personal = profile.personal_info or {}
    parts.append(personal.get("name", ""))
    parts.append(personal.get("summary", ""))

    skills = profile.skills or []
    parts.append("Skills: " + ", ".join(skills))

    for exp in (profile.experience or []):
        parts.append(f"{exp.get('role', '')} at {exp.get('company', '')} - {exp.get('description', '')}")

    for proj in (profile.projects or []):
        parts.append(f"Project: {proj.get('name', '')} - {proj.get('description', '')} ({proj.get('tech_stack', '')})")

    for cert in (profile.certifications or []):
        parts.append(f"Certification: {cert.get('name', '')} by {cert.get('issuer', '')}")

    for edu in (profile.education or []):
        parts.append(f"{edu.get('degree', '')} in {edu.get('field', '')} from {edu.get('institution', '')}")

    return " ".join(parts)


@router.post("/analyze", response_model=ATSResponse)
def analyze_ats(
    req: ATSRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compute ATS match score between user's resume/profile and a job description.

    If resume_text is provided, it uses that directly.
    Otherwise, it converts the user's stored profile to text.
    """
    # Determine the resume text to score against
    if req.resume_text:
        resume_text = req.resume_text
    else:
        # Get the most recent generated resume from history
        latest_history = (
            db.query(ResumeHistory)
            .filter(
                ResumeHistory.user_id == current_user.id,
                ResumeHistory.generation_type == "resume"
            )
            .order_by(ResumeHistory.created_at.desc())
            .first()
        )

        if latest_history and latest_history.resume_markdown:
            resume_text = latest_history.resume_markdown
        else:
            # Fall back to profile-based text
            profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No resume or profile found. Please generate a resume first."
                )
            resume_text = _profile_to_text(profile)

    try:
        score, matching, missing, suggestions = calculate_ats_score(
            resume_text=resume_text,
            job_description=req.job_description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"ATS scoring error: {str(e)}"
        )

    # Update ATS score in the latest history record
    latest = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == current_user.id,
            ResumeHistory.generation_type == "resume"
        )
        .order_by(ResumeHistory.created_at.desc())
        .first()
    )
    if latest:
        latest.ats_score = score
        db.commit()

    return ATSResponse(
        score=score,
        matching_keywords=matching,
        missing_keywords=missing,
        improvement_suggestions=suggestions
    )
