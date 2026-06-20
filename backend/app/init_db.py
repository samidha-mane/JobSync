from app.database.connection import engine, Base
from app.models.job_model import Job
from app.models.user_model import User
from app.models.resume_model import Resume

Base.metadata.create_all(bind=engine)
print("Database tables created!")