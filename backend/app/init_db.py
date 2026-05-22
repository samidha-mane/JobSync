from app.database.connection import engine
from app.models.job_model import Job
from app.database.connection import Base


Base.metadata.create_all(bind=engine)

print("Database tables created!")