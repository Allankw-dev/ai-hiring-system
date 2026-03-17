import re

FAKE_KEYWORDS = [
    "100% expert",
    "guaranteed",
    "perfect developer",
    "world best programmer"
]

SUSPICIOUS_EMAILS = [
    "@mailinator.com",
    "@tempmail.com",
    "@fakeemail.com"
]


def check_fake_resume(text):

    text_lower = text.lower()

    flags = []

    # keyword stuffing detection
    python_count = text_lower.count("python")
    if python_count > 15:
        flags.append("Keyword stuffing detected")

    # suspicious phrases
    for word in FAKE_KEYWORDS:
        if word in text_lower:
            flags.append("Suspicious exaggeration")

    # unrealistic experience
    experience = re.findall(r"(\d+)\s+years", text_lower)

    for exp in experience:
        if int(exp) > 40:
            flags.append("Unrealistic years of experience")

    return flags