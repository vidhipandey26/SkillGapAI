import functools

@functools.lru_cache(maxsize=1)
def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except:
        return None

def match_skills(resume_skills, jd_skills, threshold=0.70):
    if not resume_skills or not jd_skills:
        return [], []
    model = _load_model()
    if model:
        from sentence_transformers import util
        r = model.encode(resume_skills, convert_to_tensor=True)
        j = model.encode(jd_skills, convert_to_tensor=True)
        matched, records = set(), []
        for i, rs in enumerate(resume_skills):
            for k, js in enumerate(jd_skills):
                sim = float(util.cos_sim(r[i], j[k]))
                if sim >= threshold:
                    matched.add(js)
                    records.append((rs, js, round(sim, 3)))
        return sorted(list(matched)), records
    matched = [j for j in jd_skills if j.lower() in [r.lower() for r in resume_skills]]
    return matched, [(r, j, 1.0) for j in matched for r in resume_skills if r.lower() == j.lower()]

def compute_match_percentage(matched, jd_skills):
    return (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0

def get_missing_skills(jd_skills, matched):
    m = {s.lower() for s in matched}
    return [s for s in jd_skills if s.lower() not in m]
