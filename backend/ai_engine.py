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
    job_desc = clean_text(job_desc)
    resume_text = clean_text(resume_text)

    documents = [job_desc, resume_text]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return float(score[0][0]) * 100
