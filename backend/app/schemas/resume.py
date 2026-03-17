from pydantic import BaseModel


class ResumeOut(BaseModel):
    id: int
    file_name: str
    experience_years: float
    verification_status: str

    class Config:
        from_attributes = True