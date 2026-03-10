# Master skill database (expandable)
SKILL_DATABASE = [
    "python",
    "machine learning",
    "deep learning",
    "data analysis",
    "sql",
    "pandas",
    "scikit learn",
    "tensorflow",
    "nlp",
    "data visualization",
    "react",
    "javascript",
    "html",
    "css",
    "rest api",
    "model deployment"
]


def extract_skills(cleaned_text):
    """
    Extracts skills from cleaned text using rule-based matching
    """
    found_skills = []

    for skill in SKILL_DATABASE:
        if skill in cleaned_text:
            found_skills.append(skill)

    return list(set(found_skills))