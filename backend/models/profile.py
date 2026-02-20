"""
Profile ORM model — stores a user's structured career data as JSON.
"""
from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Structured career data stored as JSON blobs
    personal_info = Column(JSON, default={})   # name, email, phone, linkedin, github, location
    education = Column(JSON, default=[])        # list of {institution, degree, year, gpa}
    experience = Column(JSON, default=[])       # list of {company, role, duration, description}
    skills = Column(JSON, default=[])           # list of skill strings
    projects = Column(JSON, default=[])         # list of {name, tech_stack, description, link}
    certifications = Column(JSON, default=[])   # list of {name, issuer, year}
    internships = Column(JSON, default=[])      # list of {company, role, duration, description}
    achievements = Column(Text, nullable=True)  # free-text achievements

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
