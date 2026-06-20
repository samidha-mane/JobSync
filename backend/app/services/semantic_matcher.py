from sqlalchemy.orm import Session
from app.models.job_model import Job
from app.services.embedding_service import get_embedding, cosine_similarity
from app.services.skill_extractor import extract_skills

def semantic_match(db: Session, resume_text: str, top_k: int = 10) -> list[dict]:
    resume_embedding = get_embedding(resume_text)
    jobs = db.query(Job).all()
    candidate_skills = set(s.lower() for s in extract_skills(resume_text))

    results = []
    for job in jobs:
        skills_text = f"{job.title}. {', '.join(job.required_skills)}. {job.description or ''}"
        job_embedding = get_embedding(skills_text)
        score = cosine_similarity(resume_embedding, job_embedding)

        if score < 0.3:
            continue

        job_skills = set(s.lower() for s in job.required_skills)

        results.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "match_score": round(score * 100, 1),
            "matched_skills": list(job_skills & candidate_skills),
            "missing_skills": list(job_skills - candidate_skills),
            "source_url": job.source_url,
        })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)[:top_k]