"""
Profile Router — CRUD for user's career profile.
Endpoints:
  GET  /api/profile       — get current user's profile
  PUT  /api/profile       — create or update profile
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.profile import Profile
from models.user import User
from schemas.profile import ProfileUpdateRequest, ProfileResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])


def _profile_to_dict(profile: Profile) -> dict:
    """Convert a Profile ORM model to a plain dict for the response."""
    return {
        "user_id": profile.user_id,
        "personal_info": profile.personal_info or {},
        "education": profile.education or [],
        "experience": profile.experience or [],
        "skills": profile.skills or [],
        "projects": profile.projects or [],
        "certifications": profile.certifications or [],
        "internships": profile.internships or [],
        "achievements": profile.achievements,
    }


@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the authenticated user's career profile.
    Returns empty fields if profile not yet created.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        # Return empty profile structure
        return ProfileResponse(
            user_id=current_user.id,
            personal_info={},
            education=[],
            experience=[],
            skills=[],
            projects=[],
            certifications=[],
            internships=[],
            achievements=None
        )
    return _profile_to_dict(profile)


@router.put("", response_model=ProfileResponse)
def upsert_profile(
    req: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update the authenticated user's career profile.
    Performs an upsert — creates if doesn't exist, updates fields that are provided.
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()

    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    # Update only provided fields (partial update support)
    if req.personal_info is not None:
        profile.personal_info = req.personal_info.model_dump()
    if req.education is not None:
        profile.education = [e.model_dump() for e in req.education]
    if req.experience is not None:
        profile.experience = [e.model_dump() for e in req.experience]
    if req.skills is not None:
        profile.skills = req.skills
    if req.projects is not None:
        profile.projects = [p.model_dump() for p in req.projects]
    if req.certifications is not None:
        profile.certifications = [c.model_dump() for c in req.certifications]
    if req.internships is not None:
        profile.internships = [i.model_dump() for i in req.internships]
    if req.achievements is not None:
        profile.achievements = req.achievements

    db.commit()
    db.refresh(profile)
    return _profile_to_dict(profile)
