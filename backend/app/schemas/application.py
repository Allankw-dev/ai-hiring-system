from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: int


class ApplicantApplicationOut(BaseModel):
    id: int
    job_id: int
    resume_id: int
    status: str

    class Config:
        from_attributes = True