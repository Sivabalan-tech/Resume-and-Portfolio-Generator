"""
Resume Router — generates ATS-optimized resumes via LLM and manages history.
Endpoints:
  POST /api/resume/generate    — generate a resume
  GET  /api/resume/history     — get user's generation history
  GET  /api/resume/history/{id} — get specific history item
  DELETE /api/resume/history/{id} — delete history item
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
import traceback
from database import get_db
from models.user import User
from models.profile import Profile
from models.resume_history import ResumeHistory
from schemas.resume import ResumeGenerateRequest, ResumeResponse, HistoryItem
from services.auth_service import get_current_user
from services.ai_service import generate_resume

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/resume", tags=["Resume"])


def _get_profile_dict(user_id: int, db: Session) -> dict:
    """Fetch user profile as a plain dict, raise 404 if not found."""
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please complete your profile first."
        )
    return {
        "personal_info": profile.personal_info or {},
        "education": profile.education or [],
        "experience": profile.experience or [],
        "skills": profile.skills or [],
        "projects": profile.projects or [],
        "certifications": profile.certifications or [],
        "internships": profile.internships or [],
        "achievements": profile.achievements or "",
    }


@router.post("/generate", response_model=ResumeResponse)
def generate_resume_endpoint(
    req: ResumeGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate an ATS-optimized resume for the authenticated user.
    - Fetches user's profile from DB
    - Calls Gemini API with engineered prompts
    - Saves the result to resume_history
    - Returns the Markdown resume
    """
    profile_dict = _get_profile_dict(current_user.id, db)

    try:
        resume_md = generate_resume(
            profile=profile_dict,
            job_role=req.job_role,
            job_description=req.job_description or ""
        )
    except RuntimeError as e:
        logger.error(f"❌ Gemini API failed: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    # Save to history
    history_entry = ResumeHistory(
        user_id=current_user.id,
        job_role=req.job_role,
        resume_markdown=resume_md,
        generation_type="resume"
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    return ResumeResponse(
        resume_markdown=resume_md,
        job_role=req.job_role,
        history_id=history_entry.id
    )


@router.get("/history", response_model=List[HistoryItem])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return all resume/cover letter generation history for the current user."""
    history = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.user_id == current_user.id)
        .order_by(ResumeHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return history


@router.get("/history/{history_id}", response_model=ResumeResponse)
def get_history_item(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return full content of a specific history item."""
    item = db.query(ResumeHistory).filter(
        ResumeHistory.id == history_id,
        ResumeHistory.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="History item not found")

    return ResumeResponse(
        resume_markdown=item.resume_markdown or "",
        job_role=item.job_role or "",
        history_id=item.id
    )


@router.delete("/history/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history_item(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific history item for the current user."""
    item = db.query(ResumeHistory).filter(
        ResumeHistory.id == history_id,
        ResumeHistory.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(item)
    db.commit()
