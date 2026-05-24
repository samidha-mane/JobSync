import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.job_service import create_job, get_job_by_source_url


ADZUNA_BASE = "https://api.adzuna.com/v1/api/jobs"


def fetch_adzuna_jobs(
    db: Session,
    query: str,
    country: str = "in",
    pages: int = 1
):
    fetched = 0
    skipped = 0

    for page in range(1, pages + 1):

        url = f"{ADZUNA_BASE}/{country}/search/{page}"

        params = {
            "app_id": settings.adzuna_app_id,
            "app_key": settings.adzuna_app_key,
            "results_per_page": 10,
            "what": query,
            "content-type": "application/json",
        }

        response = httpx.get(url, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        for result in data.get("results", []):

            source_url = result.get("redirect_url", "")

            if get_job_by_source_url(db, source_url):
                skipped += 1
                continue

            create_job(
                db=db,
                title=result.get("title", "Untitled"),
                company=result.get("company", {}).get("display_name", "Unknown"),
                location=result.get("location", {}).get("display_name", "Remote"),
                description=result.get("description", ""),
                required_skills=extract_skills_from_description(
                    result.get("description", "")
                ),
                job_type="full-time",
                source="adzuna",
                source_url=source_url,
            )

            fetched += 1

    print(f"Fetched: {fetched}, Skipped: {skipped}")

    return fetched


def extract_skills_from_description(description: str):

    from app.services.skill_extractor import extract_skills

    return extract_skills(description)

