import json
import os
from io import BytesIO

import pdfplumber
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.services.resume_validator import check_fake_resume
from app.core.config import get_settings
from app.core.dep import get_db, get_current_user
from app.models.resume import Resume
from app.services.ai_engine import extract_skills, estimate_experience
from app.services.verifier import file_checksum, basic_resume_verification

router = APIRouter(prefix="/resumes", tags=["Resumes"])
settings = get_settings()


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    lower = filename.lower()

    if lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    if lower.endswith(".pdf"):
        parts = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        return "\n".join(parts).strip()

    raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_bytes = file.file.read()
    checksum = file_checksum(file_bytes)

    duplicate = db.query(Resume).filter(Resume.checksum == checksum).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Duplicate resume detected")

    parsed_text = extract_text_from_upload(file.filename, file_bytes)
    experience_years = estimate_experience(parsed_text)
    skills = extract_skills(parsed_text)

    verification_status, flags, _verification_score = basic_resume_verification(parsed_text)

    fake_flags = check_fake_resume(parsed_text)
    if fake_flags:
        flags.extend(fake_flags)
        verification_status = "flagged"

    save_name = f"{current_user.id}_{checksum[:10]}_{file.filename}"
    save_path = os.path.join(settings.UPLOAD_DIR, save_name)

    with open(save_path, "wb") as out_file:
        out_file.write(file_bytes)

    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=save_path,
        checksum=checksum,
        parsed_text=parsed_text,
        extracted_skills=json.dumps(skills),
        experience_years=experience_years,
        verification_status=verification_status,
        risk_flags=json.dumps(flags)
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "id": resume.id,
        "file_name": resume.file_name,
        "experience_years": resume.experience_years,
        "verification_status": resume.verification_status,
        "risk_flags": flags
    }


@router.get("/my")
def list_my_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.id.desc()).all()

    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "experience_years": r.experience_years,
            "verification_status": r.verification_status
        }
        for r in resumes
    ]