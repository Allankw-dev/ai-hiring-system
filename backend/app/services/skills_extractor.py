import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
    "linux"
]


def extract_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:
        if skill in text:
            detected.append(skill)

    return list(set(detected))