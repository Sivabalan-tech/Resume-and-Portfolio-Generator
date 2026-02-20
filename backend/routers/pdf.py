"""
PDF Router — converts generated resume markdown to downloadable PDF.
Endpoints:
  POST /api/pdf/download          — download PDF from provided markdown
  GET  /api/pdf/history/{id}      — download PDF from a history item
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from io import BytesIO
from database import get_db
from models.user import User
from models.resume_history import ResumeHistory
from services.auth_service import get_current_user
from services.pdf_service import markdown_to_pdf

router = APIRouter(prefix="/api/pdf", tags=["PDF Export"])


class PDFRequest(BaseModel):
    markdown_text: str
    filename: str = "resume"


@router.post("/download")
def download_pdf_from_markdown(
    req: PDFRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Convert provided Markdown text to PDF and return as a file download.
    The markdown can be any resume content — directly from the generate endpoint.
    """
    try:
        pdf_bytes = markdown_to_pdf(req.markdown_text)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    filename = f"{req.filename.replace(' ', '_').lower()}_resume.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/history/{history_id}")
def download_pdf_from_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download a PDF for a previously generated resume from history.
    """
    item = db.query(ResumeHistory).filter(
        ResumeHistory.id == history_id,
        ResumeHistory.user_id == current_user.id,
        ResumeHistory.generation_type == "resume"
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Resume history item not found")

    if not item.resume_markdown:
        raise HTTPException(status_code=400, detail="No resume content to convert to PDF")

    try:
        pdf_bytes = markdown_to_pdf(item.resume_markdown)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    filename = f"{(item.job_role or 'resume').replace(' ', '_').lower()}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
