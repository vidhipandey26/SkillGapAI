skills = [
"python",
"machine learning",
"deep learning",
"sql",
"pandas",
"data visualization",
"nlp",
"tensorflow",
"pytorch",
"matplotlib",
"seaborn"
]

skill_alias = {
"pytorch": "deep learning",
"tensorflow": "deep learning",
"matplotlib": "data visualization",
"seaborn": "data visualization"
}

def extract_skills(text):

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    for alias, parent in skill_alias.items():
        if alias in text and parent not in found_skills:
            found_skills.append(parent)

    return list(set(found_skills))