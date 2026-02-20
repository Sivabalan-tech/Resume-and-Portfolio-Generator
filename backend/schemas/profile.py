"""
Pydantic schemas for the user profile module.
"""
from pydantic import BaseModel
from typing import Optional, List, Any


class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    location: str = ""
    website: str = ""
    summary: str = ""


class EducationItem(BaseModel):
    institution: str = ""
    degree: str = ""
    field: str = ""
    year_start: str = ""
    year_end: str = ""
    gpa: str = ""


class ExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""
    location: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    tech_stack: str = ""
    description: str = ""
    link: str = ""


class CertificationItem(BaseModel):
    name: str = ""
    issuer: str = ""
    year: str = ""
    link: str = ""


class InternshipItem(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class ProfileUpdateRequest(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    education: Optional[List[EducationItem]] = None
    experience: Optional[List[ExperienceItem]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[ProjectItem]] = None
    certifications: Optional[List[CertificationItem]] = None
    internships: Optional[List[InternshipItem]] = None
    achievements: Optional[str] = None


class ProfileResponse(BaseModel):
    user_id: int
    personal_info: Any = {}
    education: Any = []
    experience: Any = []
    skills: Any = []
    projects: Any = []
    certifications: Any = []
    internships: Any = []
    achievements: Optional[str] = None

    class Config:
        from_attributes = True
