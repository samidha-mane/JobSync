from typing import List

from app.models.job_model import Job


def match_jobs(
    candidate_skills: List[str],
    jobs: List[Job]
) -> List[dict]:

    candidate_set = set(

        skill.lower()

        for skill in candidate_skills
    )

    results = []


    for job in jobs:

        job_skills = set(

            skill.lower()

            for skill in job.required_skills
        )

        matched = candidate_set & job_skills

        missing = job_skills - candidate_set


        if len(job_skills) > 0:

            match_percentage = round(

                (len(matched) / len(job_skills)) * 100,
                1
            )

        else:

            match_percentage = 0


        results.append({

            "job_id": job.id,

            "title": job.title,

            "company": job.company,

            "location": job.location,

            "match_percentage": match_percentage,

            "matched_skills": list(matched),

            "missing_skills": list(missing)

        })


    results.sort(

        key=lambda x: x["match_percentage"],

        reverse=True
    )

    return results