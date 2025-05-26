from typing import List
from datetime import date

from pydantic import BaseModel, HttpUrl, EmailStr


class Contact(BaseModel):
    name: str
    email: EmailStr
    portfolio: HttpUrl | None = None
    github: HttpUrl | None = None


class SkillCategory(BaseModel):
    category: str  # e.g. "Frameworks", "Languages"
    skills: List[str]


class Experience(BaseModel):
    title: str
    company: str
    location: str
    start_date: date
    end_date: date | None = None
    bullets: List[str]


class Project(BaseModel):
    title: str
    url: HttpUrl | None = None
    bullets: List[str]


class Education(BaseModel):
    school: str
    degree: str
    field: str
    graduation_date: date


class Resume(BaseModel):
    contact: Contact
    summary: str | None = None
    skills: List[SkillCategory]
    experience: List[Experience]
    projects: List[Project]
    education: List[Education]
