"""
matcher.py
Semantic skill matching using sentence-transformers (all-MiniLM-L6-v2).
Falls back to exact/fuzzy string matching if model unavailable.
"""
from typing import List, Tuple
import functools

SIMILARITY_THRESHOLD = 0.70


@functools.lru_cache(maxsize=1)
def _load_model():
    """Lazily load the sentence transformer model (cached after first load)."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model
    except Exception as e:
        print(f"[SentenceTransformer] could not load model: {e}")
        return None


def match_skills(
    resume_skills: List[str],
    jd_skills: List[str],
    threshold: float = SIMILARITY_THRESHOLD
) -> Tuple[List[str], List[Tuple[str, str, float]]]:
    """
    Semantically match resume skills to JD skills.

    Returns:
        matched_skills: list of JD skills that were matched
        similarity_scores: list of (resume_skill, jd_skill, score) for matched pairs
    """
    if not resume_skills or not jd_skills:
        return [], []

    model = _load_model()

    if model is not None:
        return _semantic_match(model, resume_skills, jd_skills, threshold)
    else:
        return _fallback_match(resume_skills, jd_skills)


def _semantic_match(model, resume_skills, jd_skills, threshold):
    """Use cosine similarity of sentence embeddings."""
    from sentence_transformers import util

    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

    matched_jd = set()
    similarity_records = []

    for i, r_skill in enumerate(resume_skills):
        for j, j_skill in enumerate(jd_skills):
            sim = float(util.cos_sim(resume_embeddings[i], jd_embeddings[j]))
            if sim >= threshold:
                if j_skill not in matched_jd:
                    matched_jd.add(j_skill)
                similarity_records.append((r_skill, j_skill, round(sim, 3)))

    # Keep only the best match per pair
    similarity_records.sort(key=lambda x: x[2], reverse=True)

    return sorted(list(matched_jd)), similarity_records


def _fallback_match(resume_skills, jd_skills):
    """Simple string containment fallback when model is unavailable."""
    matched = []
    records = []
    r_lower = {s.lower(): s for s in resume_skills}

    for j_skill in jd_skills:
        j_lower = j_skill.lower()
        if j_lower in r_lower:
            matched.append(j_skill)
            records.append((r_lower[j_lower], j_skill, 1.0))
        else:
            # Partial match
            for r_key, r_orig in r_lower.items():
                if j_lower in r_key or r_key in j_lower:
                    matched.append(j_skill)
                    records.append((r_orig, j_skill, 0.75))
                    break

    return sorted(list(set(matched))), records


def compute_match_percentage(matched_skills: List[str], jd_skills: List[str]) -> float:
    """Return match percentage (0–100)."""
    if not jd_skills:
        return 0.0
    return (len(matched_skills) / len(jd_skills)) * 100


def get_missing_skills(jd_skills: List[str], matched_skills: List[str]) -> List[str]:
    """Return JD skills not found in the resume."""
    matched_lower = {s.lower() for s in matched_skills}
    return [s for s in jd_skills if s.lower() not in matched_lower]