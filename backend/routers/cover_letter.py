"""
Cover Letter Router — generates personalized cover letters.
Endpoints:
  POST /api/cover-letter/generate   — generate cover letter
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.profile import Profile
from models.resume_history import ResumeHistory
from schemas.resume import CoverLetterRequest, CoverLetterResponse
from services.auth_service import get_current_user
from services.ai_service import generate_cover_letter

router = APIRouter(prefix="/api/cover-letter", tags=["Cover Letter"])


@router.post("/generate", response_model=CoverLetterResponse)
def generate_cover_letter_endpoint(
    req: CoverLetterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a tailored cover letter for a specific company and job role.
    - Uses user's profile as context
    - Calls Gemini API with the cover letter prompt
    - Saves to history
    """
    # Fetch profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please complete your profile first."
        )

    profile_dict = {
        "personal_info": profile.personal_info or {},
        "skills": profile.skills or [],
        "experience": profile.experience or [],
        "projects": profile.projects or [],
    }

    try:
        letter = generate_cover_letter(
            profile=profile_dict,
            company_name=req.company_name,
            job_role=req.job_role,
            job_description=req.job_description,
            hiring_manager=req.hiring_manager or "Hiring Manager"
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    # Save to history
    history_entry = ResumeHistory(
        user_id=current_user.id,
        job_role=req.job_role,
        company_name=req.company_name,
        cover_letter=letter,
        generation_type="cover_letter"
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    return CoverLetterResponse(
        cover_letter=letter,
        company_name=req.company_name,
        history_id=history_entry.id
    )


@router.get("/history/{history_id}", response_model=CoverLetterResponse)
def get_cover_letter_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve a previously generated cover letter by history ID."""
    item = db.query(ResumeHistory).filter(
        ResumeHistory.id == history_id,
        ResumeHistory.user_id == current_user.id,
        ResumeHistory.generation_type == "cover_letter"
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Cover letter not found.")

    return CoverLetterResponse(
        cover_letter=item.cover_letter or "",
        company_name=item.company_name or "",
        history_id=item.id
    )
