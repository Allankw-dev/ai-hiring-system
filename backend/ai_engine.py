import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Clean text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Estimate years of experience


def estimate_experience(text):
    matches = re.findall(r'(\d+)\s+years', text.lower())
    if matches:
        return max([int(year) for year in matches])
    return 0

# Calculate similarity score


def calculate_similarity(job_desc, resume_text):

    job_desc_clean = clean_text(job_desc)
    resume_clean = clean_text(resume_text)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_desc_clean, resume_clean])

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:2]
    )

    similarity_percentage = float(similarity_score[0][0]) * 100

    # -------- Skill Matching --------
    required_skills = ["python", "fastapi", "sql"]
    resume_lower = resume_text.lower()

    matched_skills = sum(
        1 for skill in required_skills if skill in resume_lower
    )

    skill_match_percentage = (
        matched_skills / len(required_skills)
    ) * 100

    # -------- Experience Matching --------
    job_experience = estimate_experience(job_desc)
    resume_experience = estimate_experience(resume_text)

    if job_experience > 0:
        experience_match = min(
            resume_experience / job_experience,
            1
        ) * 100
    else:
        experience_match = 100

    # -------- Final Weighted Score --------
    final_score = (
        0.7 * similarity_percentage
        + 0.2 * skill_match_percentage
        + 0.1 * experience_match
    )

    return {
        "final_score": round(final_score, 2),
        "similarity_score": round(similarity_percentage, 2),
        "skill_match": round(skill_match_percentage, 2),
        "experience_match": round(experience_match, 2)
    }
