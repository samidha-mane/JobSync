from sqlalchemy.orm import Session
from app.models.job_model import Job

from typing import List, Optional


def get_all_jobs(db: Session) -> List[Job]:

    return db.query(Job).all()


def get_job_by_id(db: Session, job_id: int) -> Optional[Job]:

    return db.query(Job).filter(Job.id == job_id).first()


def create_job(
    db: Session,
    title: str,
    company: str,
    location: str,
    required_skills: List[str],
    description: str = None,
    job_type: str = "full-time",
    source: str = "manual",
    source_url: str = None
) -> Job:

    new_job = Job(

        title=title,
        company=company,
        location=location,

        required_skills=required_skills,

        description=description,
        job_type=job_type,

        source=source,
        source_url=source_url
    )

    db.add(new_job)

    db.commit()

    db.refresh(new_job)

    return new_job


def search_jobs_by_skills(
    db: Session,
    skills: List[str]
) -> List[Job]:

    return db.query(Job).filter(

        Job.required_skills.overlap(skills)

    ).all()