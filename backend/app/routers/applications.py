from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dep import get_db, get_current_user
from app.models.job import Job
from app.models.resume import Resume
from app.models.application import Application
from app.schemas.application import ApplicationCreate
from app.services.ai_engine import calculate_match
from app.services.verifier import basic_resume_verification

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/")
def apply_to_job(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        job = db.query(Job).filter(Job.id == payload.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        resume = db.query(Resume).filter(
            Resume.id == payload.resume_id,
            Resume.user_id == current_user.id
        ).first()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        existing_application = db.query(Application).filter(
            Application.user_id == current_user.id,
            Application.job_id == payload.job_id,
            Application.resume_id == payload.resume_id
        ).first()

        if existing_application:
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job with this resume"
            )

        _status, _flags, verification_score = basic_resume_verification(resume.parsed_text)

        result = calculate_match(
            job_desc=job.description,
            resume_text=resume.parsed_text,
            verification_score=verification_score
        )

        application = Application(
            user_id=current_user.id,
            job_id=job.id,
            resume_id=resume.id,
            ai_score=result["overall_score"],
            status="submitted"
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return {
            "application_id": application.id,
            "job_id": job.id,
            "resume_id": resume.id,
            "ai_score": application.ai_score,
            "status": application.status
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my")
def list_my_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return db.query(Application).filter(
            Application.user_id == current_user.id
        ).order_by(Application.id.desc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))