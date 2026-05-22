from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from sqlalchemy.sql import func
from app.database.connection import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200), nullable=True)
    job_type = Column(String(50), nullable=True)   
    
    description = Column(Text, nullable=True)
    
    required_skills = Column(ARRAY(String), nullable=False, default=[])
    
    
    source = Column(String(100), nullable=True, default="manual")
    source_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())