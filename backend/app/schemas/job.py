from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: str = ""
    min_experience: float = 0


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    required_skills: str | None = None
    min_experience: float

    class Config:
        from_attributes = True