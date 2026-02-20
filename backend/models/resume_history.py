"""
ResumeHistory ORM model — logs every AI-generated resume for a user.
"""
from sqlalchemy import Column, Integer, ForeignKey, Text, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_role = Column(String, nullable=True)          # e.g. "Backend Developer"
    company_name = Column(String, nullable=True)      # used for cover letters
    resume_markdown = Column(Text, nullable=True)     # generated resume (markdown)
    cover_letter = Column(Text, nullable=True)        # generated cover letter
    ats_score = Column(Integer, nullable=True)        # 0–100
    generation_type = Column(String, default="resume")  # resume | cover_letter | portfolio
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resume_history")
