from utils.parser import extract_text_from_pdf
from utils.embedder import get_embedding, get_similarity_score

# Read JD
jd_text = open("job_descriptions/JD1.txt").read()
jd_embedding = get_embedding(jd_text)

# Read Resume
resume_text = extract_text_from_pdf("resumes/data_analyst_resume_1.pdf")
resume_embedding = get_embedding(resume_text)

# Compare
score = get_similarity_score(jd_embedding, resume_embedding)
print(f"Match Score: {score:.2f}")
