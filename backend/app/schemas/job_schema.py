from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JobCreate(BaseModel):

    title: str
    company: str
    location: str

    required_skills: List[str]

    description: Optional[str] = None
    job_type: Optional[str] = "full-time"

    source_url: Optional[str] = None


class JobRead(BaseModel):

    id: int

    title: str
    company: str
    location: str

    required_skills: List[str]

    description: Optional[str]
    job_type: Optional[str]

    source: Optional[str]
    source_url: Optional[str]

    created_at: Optional[datetime]

    class Config:

        from_attributes = True