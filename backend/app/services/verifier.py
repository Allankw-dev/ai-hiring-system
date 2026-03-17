import hashlib
import re


def file_checksum(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def basic_resume_verification(parsed_text: str):
    flags = []
    verification_score = 100.0

    text = parsed_text.strip()

    if len(text) < 120:
        flags.append("resume_too_short")
        verification_score -= 25

    if text.lower().count("python") > 25:
        flags.append("possible_keyword_stuffing")
        verification_score -= 20

    years_found = re.findall(r"\b(?:19|20)\d{2}\b", text)
    if len(years_found) > 18:
        flags.append("many_dates_detected_review_needed")
        verification_score -= 10

    if "@" not in text:
        flags.append("contact_info_missing")
        verification_score -= 10

    status = "verified" if verification_score >= 80 else "flagged"
    return status, flags, max(0.0, verification_score)