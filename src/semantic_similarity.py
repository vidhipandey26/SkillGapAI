from sentence_transformers import SentenceTransformer, util

# Load pretrained semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(resume_text, job_text):

    embeddings = model.encode(
        [resume_text, job_text],
        convert_to_tensor=True
    )

    similarity_score = util.cos_sim(
        embeddings[0],
        embeddings[1]
    )

    return round(float(similarity_score * 100), 2)