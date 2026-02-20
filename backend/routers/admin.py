"""
Admin Router — admin-only endpoints for user management and platform analytics.
Endpoints:
  GET /api/admin/users      — list all registered users
  GET /api/admin/stats      — platform-wide statistics
  DELETE /api/admin/users/{id} — delete a user
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from models.user import User, UserRole
from models.profile import Profile
from models.resume_history import ResumeHistory
from services.auth_service import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class UserAdminView(BaseModel):
    id: int
    email: str
    full_name: str | None
    role: UserRole
    created_at: datetime
    has_profile: bool
    resume_count: int

    class Config:
        from_attributes = True


class PlatformStats(BaseModel):
    total_users: int
    total_resumes_generated: int
    total_cover_letters_generated: int
    total_portfolios_generated: int
    avg_ats_score: float
    new_users_today: int


@router.get("/users", response_model=List[UserAdminView])
def list_all_users(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin: List all registered users with profile and activity stats.
    Requires admin role.
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    result = []

    for user in users:
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        resume_count = (
            db.query(ResumeHistory)
            .filter(ResumeHistory.user_id == user.id)
            .count()
        )
        result.append(UserAdminView(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at,
            has_profile=profile is not None,
            resume_count=resume_count
        ))

    return result


@router.get("/stats", response_model=PlatformStats)
def get_platform_stats(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin: Get platform-wide analytics and statistics.
    """
    today = datetime.utcnow().date()

    total_users = db.query(User).count()

    total_resumes = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.generation_type == "resume")
        .count()
    )
    total_cover_letters = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.generation_type == "cover_letter")
        .count()
    )
    total_portfolios = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.generation_type == "portfolio")
        .count()
    )

    avg_ats_result = (
        db.query(func.avg(ResumeHistory.ats_score))
        .filter(ResumeHistory.ats_score.isnot(None))
        .scalar()
    )
    avg_ats = round(float(avg_ats_result), 1) if avg_ats_result else 0.0

    new_today = (
        db.query(User)
        .filter(func.date(User.created_at) == today)
        .count()
    )

    return PlatformStats(
        total_users=total_users,
        total_resumes_generated=total_resumes,
        total_cover_letters_generated=total_cover_letters,
        total_portfolios_generated=total_portfolios,
        avg_ats_score=avg_ats,
        new_users_today=new_today
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin: Delete a user account and all associated data.
    Cannot delete yourself.
    """
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Cascade delete associated data
    db.query(ResumeHistory).filter(ResumeHistory.user_id == user_id).delete()
    db.query(Profile).filter(Profile.user_id == user_id).delete()
    db.delete(user)
    db.commit()
