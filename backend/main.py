from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal, Candidate
from ai_engine import calculate_similarity, estimate_experience

app = FastAPI()

# New Data Model


class CandidateData(BaseModel):
    name: str
    resume_text: str
    job_description: str


@app.get("/")
def home():
    return {"message": "AI Hiring System with Intelligence 🚀"}


@app.post("/analyze")
def analyze_candidate(data: CandidateData):
    score = calculate_similarity(
        data.job_description,
        data.resume_text
    )

    experience = estimate_experience(data.resume_text)

    db = SessionLocal()

    candidate = Candidate(
        name=data.name,
        match_score=score,
        experience=experience
    )

    db.add(candidate)
    db.commit()

    return {
        "name": data.name,
        "match_score": score,
        "experience": experience
    }


@app.get("/candidates")
def get_candidates():
    db = SessionLocal()
    candidates = db.query(Candidate).all()

    return [
        {
            "name": c.name,
            "match_score": c.match_score,
            "experience": c.experience
        }
        for c in candidates
    ]
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)