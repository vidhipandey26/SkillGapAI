import functools
from typing import List, Tuple

SIMILARITY_THRESHOLD = 0.70

@functools.lru_cache(maxsize=1)
def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Model load failed: {e}")
        return None

def match_skills(resume_skills, jd_skills, threshold=SIMILARITY_THRESHOLD):
    if not resume_skills or not jd_skills:
        return [], []
    model = _load_model()
    if model:
        return _semantic_match(model, resume_skills, jd_skills, threshold)
    return _fallback_match(resume_skills, jd_skills)

def _semantic_match(model, resume_skills, jd_skills, threshold):
    from sentence_transformers import util
    r_emb = model.encode(resume_skills, convert_to_tensor=True)
    j_emb = model.encode(jd_skills, convert_to_tensor=True)
    matched_jd = set()
    records = []
    for i, r in enumerate(resume_skills):
        for j, jd in enumerate(jd_skills):
            sim = float(util.cos_sim(r_emb[i], j_emb[j]))
            if sim >= threshold:
                matched_jd.add(jd)
                records.append((r, jd, round(sim, 3)))
    return sorted(list(matched_jd)), sorted(records, key=lambda x: x[2], reverse=True)

def _fallback_match(resume_skills, jd_skills):
    matched, records = [], []
    r_lower = {s.lower(): s for s in resume_skills}
    for j in jd_skills:
        if j.lower() in r_lower:
            matched.append(j)
            records.append((r_lower[j.lower()], j, 1.0))
    return sorted(list(set(matched))), records

def compute_match_percentage(matched, jd_skills):
    if not jd_skills:
        return 0.0
    return (len(matched) / len(jd_skills)) * 100

def get_missing_skills(jd_skills, matched_skills):
    matched_lower = {s.lower() for s in matched_skills}
    return [s for s in jd_skills if s.lower() not in matched_lower]
