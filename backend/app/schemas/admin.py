from pydantic import BaseModel, EmailStr


class CandidateEmailRequest(BaseModel):
    application_id: int
    subject: str
    message_body: str


class CandidateRankingOut(BaseModel):
    application_id: int
    applicant_name: str
    applicant_email: EmailStr
    job_title: str
    company: str
    overall_score: float
    semantic_score: float
    skills_score: float
    experience_score: float
    verification_score: float
    status: str