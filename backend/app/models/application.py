from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Application(Base):
    __tablename__ = "Applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("Jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("Resumes.id"), nullable=False)
    overall_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    ai_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    verification_score = Column(Float, nullable=False)
    status = Column(String(50), default="submitted")
    created_at = Column(DateTime, server_default=func.getdate())