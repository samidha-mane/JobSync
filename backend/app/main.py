from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from app.services.job_fetcher import fetch_adzuna_jobs
from sqlalchemy.orm import Session

import PyPDF2
import io

from typing import List

from app.database.connection import get_db

from app.schemas.job_schema import JobCreate, JobRead

from app.services.job_service import (
    get_all_jobs,
    get_job_by_id,
    create_job
)

from app.services.skill_extractor import extract_skills

from app.services.job_matcher import match_jobs


app = FastAPI(
    title="JobSync API",
    version="1.0.0"
)


# -----------------------------------
# ROOT ROUTE
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "JobSync API is running"
    }


# -----------------------------------
# GET ALL JOBS
# -----------------------------------

@app.get("/jobs", response_model=List[JobRead])
def list_jobs(
    db: Session = Depends(get_db)
):

    return get_all_jobs(db)


# -----------------------------------
# GET SINGLE JOB
# -----------------------------------

@app.get("/jobs/{job_id}", response_model=JobRead)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = get_job_by_id(db, job_id)

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# -----------------------------------
# CREATE JOB
# -----------------------------------

@app.post("/jobs", response_model=JobRead)
def add_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):

    return create_job(
        db=db,
        title=job.title,
        company=job.company,
        location=job.location,
        required_skills=job.required_skills,
        description=job.description,
        job_type=job.job_type,
        source_url=job.source_url
    )


# -----------------------------------
# MATCH RESUME
# -----------------------------------

@app.post("/match")
async def match_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    contents = await file.read()

    pdf_reader = PyPDF2.PdfReader(
        io.BytesIO(contents)
    )

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + " "


    extracted_skills = extract_skills(text)

    jobs = get_all_jobs(db)

    matches = match_jobs(
        extracted_skills,
        jobs
    )

    return {

        "filename": file.filename,

        "extracted_skills": extracted_skills,

        "matches": matches
    }

@app.post("/admin/fetch-jobs")
def trigger_job_fetch(
    query: str = "Python developer",
    db: Session = Depends(get_db)
):

    count = fetch_adzuna_jobs(db, query=query)

    return {
        "message": f"Fetched {count} new jobs",
        "query": query
    }