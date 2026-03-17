import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COMMON_SKILLS = [
    "python", "fastapi", "flask", "django", "sql", "sql server",
    "mysql", "postgresql", "mongodb", "docker", "kubernetes",
    "git", "github", "machine learning", "nlp", "pandas", "numpy",
    "scikit-learn", "data analysis", "api", "rest api",
    "javascript", "react", "html", "css", "excel"
]


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def estimate_experience(text: str) -> float:
    matches = re.findall(r"(\d+)\s+(?:years|year)", text.lower())
    if matches:
        return float(max(int(x) for x in matches))
    return 0.0


def extract_skills(text: str) -> list[str]:
    lower = text.lower()
    found = [skill for skill in COMMON_SKILLS if skill in lower]
    return sorted(set(found))


def calculate_match(job_desc: str, resume_text: str, verification_score: float = 100.0):
    job_clean = clean_text(job_desc)
    resume_clean = clean_text(resume_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )
    tfidf_matrix = vectorizer.fit_transform([job_clean, resume_clean])
    semantic_score = float(
        cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    ) * 100

    job_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume_text)

    if job_skills:
        matched = len([s for s in job_skills if s in resume_skills])
        skills_score = (matched / len(job_skills)) * 100
    else:
        skills_score = 100.0

    job_exp = estimate_experience(job_desc)
    resume_exp = estimate_experience(resume_text)

    if job_exp > 0:
        experience_score = min(resume_exp / job_exp, 1.0) * 100
    else:
        experience_score = 100.0

    overall_score = (
        0.50 * semantic_score +
        0.25 * skills_score +
        0.15 * experience_score +
        0.10 * verification_score
    )

    missing_skills = [s for s in job_skills if s not in resume_skills]

    return {
        "overall_score": round(overall_score, 2),
        "semantic_score": round(semantic_score, 2),
        "skills_score": round(skills_score, 2),
        "experience_score": round(experience_score, 2),
        "verification_score": round(verification_score, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "resume_experience": resume_exp
    }