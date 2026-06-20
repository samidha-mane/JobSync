from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.user_schema import UserSignup, UserLogin, UserRead, TokenResponse
from app.schemas.job_schema import JobCreate, JobRead
from app.services.auth_service import get_user_by_email, create_user, verify_password, create_access_token
from app.services.job_service import get_all_jobs, create_job, get_job_by_id
from app.services.semantic_matcher import semantic_match
from app.services.skill_extractor import extract_skills
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.models.resume_model import Resume
from typing import List
import PyPDF2, io
from app.services.job_fetcher import fetch_adzuna_jobs

app = FastAPI(title="JobSync API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth ---

@app.post("/auth/signup", response_model=UserRead, status_code=201)
def signup(body: UserSignup, db: Session = Depends(get_db)):
    if get_user_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, body.email, body.full_name, body.password)

@app.post("/auth/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# --- Jobs ---

@app.get("/jobs", response_model=List[JobRead])
def list_jobs(db: Session = Depends(get_db)):
    return get_all_jobs(db)

@app.post("/jobs", response_model=JobRead, status_code=201)
def add_job(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, **job.dict())

# --- Match ---

@app.post("/match")
async def match_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contents = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)

    extracted_skills = extract_skills(resume_text)
    matches = semantic_match(db, resume_text, top_k=10)

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        raw_text=resume_text,
        extracted_skills=extracted_skills,
    )
    db.add(resume)
    db.commit()

    return {
        "user": current_user.email,
        "extracted_skills": extracted_skills,
        "total_matches": len(matches),
        "matches": matches,
    }

# --- Dashboard ---

@app.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id)\
                              .order_by(Resume.created_at.desc()).all()
    return {
        "user": current_user.email,
        "total_uploads": len(resumes),
        "history": [
            {
                "resume_id": r.id,
                "filename": r.filename,
                "skills": r.extracted_skills,
                "uploaded_at": r.created_at,
            }
            for r in resumes
        ]
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