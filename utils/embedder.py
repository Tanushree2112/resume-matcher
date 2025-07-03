from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode([text])[0]

def get_similarity_score(jd_emb, resume_emb):
    return cosine_similarity([jd_emb], [resume_emb])[0][0]
