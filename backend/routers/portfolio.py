"""
Portfolio Router — generates portfolio website content and downloadable HTML site.
Endpoints:
  POST /api/portfolio/generate      — generate portfolio content (JSON)
  POST /api/portfolio/download      — generate + download as full HTML website
  GET  /api/portfolio/download/{id} — re-download HTML from a saved history entry
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.profile import Profile
from models.resume_history import ResumeHistory
from schemas.resume import PortfolioResponse
from services.auth_service import get_current_user
from services.ai_service import generate_portfolio
from services.portfolio_html_service import generate_portfolio_html
import json

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])


def _get_profile(user_id: int, db: Session):
    """Fetch profile ORM object, raise 404 if missing."""
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please complete your profile first."
        )
    return profile


def _profile_dict(profile: Profile) -> dict:
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


@router.post("/generate", response_model=PortfolioResponse)
def generate_portfolio_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate complete portfolio content from the user's profile (JSON response).
    Returns: About Me, bio, LinkedIn summary, project descriptions, GitHub highlights.
    """
    profile = _get_profile(current_user.id, db)
    pd = _profile_dict(profile)

    try:
        portfolio_data = generate_portfolio(pd)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    # Save to history (store full portfolio JSON for later re-download)
    history_entry = ResumeHistory(
        user_id=current_user.id,
        generation_type="portfolio",
        resume_markdown=json.dumps(portfolio_data)  # store full data for re-download
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    return PortfolioResponse(
        about_me=portfolio_data.get("about_me", ""),
        professional_bio=portfolio_data.get("professional_bio", ""),
        linkedin_summary=portfolio_data.get("linkedin_summary", ""),
        project_descriptions=portfolio_data.get("project_descriptions", []),
        github_highlights=portfolio_data.get("github_highlights", ""),
        history_id=history_entry.id
    )


@router.post("/download")
def download_portfolio_website(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate portfolio content and return it as a complete downloadable HTML website.
    The HTML file is self-contained — no external dependencies, ready to host anywhere.
    """
    profile = _get_profile(current_user.id, db)
    pd = _profile_dict(profile)

    try:
        portfolio_data = generate_portfolio(pd)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    # Build the HTML website
    html_content = generate_portfolio_html(portfolio_data, pd)

    # Save to history for re-download later
    name = pd.get("personal_info", {}).get("name", "portfolio")
    history_entry = ResumeHistory(
        user_id=current_user.id,
        generation_type="portfolio",
        resume_markdown=json.dumps(portfolio_data)
    )
    db.add(history_entry)
    db.commit()

    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_').lower()
    filename = f"{safe_name}_portfolio.html"

    return Response(
        content=html_content,
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/download/{history_id}")
def re_download_portfolio(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Re-download the HTML portfolio website from a previously generated history entry.
    """
    profile = _get_profile(current_user.id, db)
    pd = _profile_dict(profile)

    item = db.query(ResumeHistory).filter(
        ResumeHistory.id == history_id,
        ResumeHistory.user_id == current_user.id,
        ResumeHistory.generation_type == "portfolio"
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio history item not found.")

    try:
        portfolio_data = json.loads(item.resume_markdown or "{}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not parse saved portfolio data.")

    html_content = generate_portfolio_html(portfolio_data, pd)
    name = pd.get("personal_info", {}).get("name", "portfolio")
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_').lower()

    return Response(
        content=html_content,
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}_portfolio.html"'}
    )
