"""
skill_extractor.py
Extracts skills from text using a curated skills dataset + spaCy NLP.
"""
import re
from typing import List

# ─── Comprehensive Skills Dataset ───────────────────────────────────────────
SKILLS_DB = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "golang",
    "rust", "kotlin", "swift", "scala", "r", "matlab", "perl", "php", "ruby",
    "bash", "shell", "powershell", "dart", "lua", "haskell", "elixir",

    # ML / AI
    "machine learning", "deep learning", "neural networks", "natural language processing",
    "nlp", "computer vision", "reinforcement learning", "transfer learning",
    "generative ai", "large language models", "llm", "transformers",
    "feature engineering", "model deployment", "mlops", "rag",
    "prompt engineering", "fine-tuning",

    # ML Frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost",
    "lightgbm", "hugging face", "fastai", "spacy", "nltk", "opencv",
    "sentence-transformers", "langchain", "llamaindex",

    # Data
    "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "cassandra", "neo4j", "sqlite", "oracle", "data warehousing", "etl",
    "data pipeline", "data engineering", "data science", "data analysis",
    "data visualization", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
    "plotly", "tableau", "power bi", "looker",

    # Cloud – Azure
    "azure", "microsoft azure", "azure ml", "azure machine learning",
    "azure blob storage", "azure devops", "azure functions", "azure kubernetes",
    "azure openai", "azure cognitive services", "azure data factory",
    "azure synapse", "azure databricks",

    # Cloud – AWS
    "aws", "amazon web services", "ec2", "s3", "lambda", "sagemaker",
    "rds", "dynamodb", "eks", "ecs", "cloudformation",

    # Cloud – GCP
    "gcp", "google cloud", "bigquery", "vertex ai", "cloud run",
    "cloud functions", "dataflow",

    # DevOps / MLOps
    "docker", "kubernetes", "ci/cd", "github actions", "jenkins", "terraform",
    "ansible", "helm", "gitlab ci", "circleci", "mlflow", "kubeflow",
    "airflow", "prefect", "dagster",

    # APIs & Backend
    "rest api", "restful", "graphql", "fastapi", "flask", "django", "express",
    "spring boot", "node.js", "microservices", "api development",

    # Frontend
    "react", "vue", "angular", "next.js", "html", "css", "tailwind",
    "streamlit", "gradio", "dash",

    # Version Control
    "git", "github", "gitlab", "bitbucket",

    # Big Data
    "spark", "apache spark", "hadoop", "kafka", "flink", "databricks",
    "hive", "pig",

    # Statistics / Math
    "statistics", "probability", "linear algebra", "calculus",
    "hypothesis testing", "a/b testing", "regression", "classification",
    "clustering", "time series", "forecasting",

    # Soft Skills (often in JDs)
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "project management", "agile", "scrum",

    # Certifications
    "aws certified", "azure certified", "google certified", "pmp",
]

# Build a sorted-by-length list for greedy matching (longer phrases first)
_SORTED_SKILLS = sorted(SKILLS_DB, key=len, reverse=True)


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from raw text.
    Uses multi-word phrase matching (greedy, longest-first).
    Returns deduplicated list of found skills.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = set()

    # ── Phrase matching ──────────────────────────────────────────────────────
    for skill in _SORTED_SKILLS:
        # Use word boundary matching for single words, substring for phrases
        if " " in skill:
            if skill in text_lower:
                found.add(skill)
        else:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.add(skill)

    return sorted(list(found))