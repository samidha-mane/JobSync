from app.database.connection import SessionLocal

from app.services.job_service import create_job


SEED_JOBS = [

    {
        "title": "Backend Python Developer",

        "company": "Razorpay",

        "location": "Bangalore",

        "required_skills": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "REST API"
        ],

        "job_type": "full-time",

        "description": "Build scalable backend APIs using Python and FastAPI.",

        "source": "manual"
    },


    {
        "title": "Full Stack Developer",

        "company": "Swiggy",

        "location": "Hyderabad",

        "required_skills": [
            "React",
            "Node.js",
            "MongoDB",
            "AWS"
        ],

        "job_type": "full-time",

        "description": "Develop scalable frontend and backend systems.",

        "source": "manual"
    },


    {
        "title": "Software Engineering Intern",

        "company": "Microsoft",

        "location": "Remote",

        "required_skills": [
            "Python",
            "DSA",
            "SQL",
            "Git"
        ],

        "job_type": "internship",

        "description": "Work on scalable cloud and backend systems.",

        "source": "manual"
    }

]


def seed_jobs():

    db = SessionLocal()

    try:

        for job_data in SEED_JOBS:

            create_job(

                db=db,

                title=job_data["title"],

                company=job_data["company"],

                location=job_data["location"],

                required_skills=job_data["required_skills"],

                description=job_data["description"],

                job_type=job_data["job_type"],

                source=job_data["source"]
            )

            print(

                f"Inserted: {job_data['title']} at {job_data['company']}"
            )

    finally:

        db.close()


if __name__ == "__main__":

    seed_jobs()