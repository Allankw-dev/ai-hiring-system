import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")


def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


def calculate_similarity(job_description, resume_text):

    job = preprocess(job_description)
    resume = preprocess(resume_text)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([job, resume])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])

    score = float(similarity[0][0]) * 100

    return round(score, 2)