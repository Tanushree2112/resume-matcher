# import streamlit as st
# import os
# from utils.parser import extract_text_from_pdf
# from utils.embedder import get_embedding, get_similarity_score

# st.title("🔍 Resume Matcher")

# # --- Upload Resumes ---
# uploaded_files = st.file_uploader(
#     "📤 Upload PDF Resumes", type=["pdf"], accept_multiple_files=True
# )

# # Save uploaded resumes to the /resumes folder
# if uploaded_files:
#     import os
#     os.makedirs("resumes", exist_ok=True)
#     for uploaded_file in uploaded_files:
#         with open(f"resumes/{uploaded_file.name}", "wb") as f:
#             f.write(uploaded_file.getbuffer())
#     st.success(f"✅ Uploaded {len(uploaded_files)} resume(s) to /resumes")

# jd_text = st.text_area("Paste Job Description Here")

# if jd_text:
#     jd_embedding = get_embedding(jd_text)

#     results = []
#     for file_name in os.listdir("resumes"):
#         file_path = os.path.join("resumes", file_name)
#         resume_text = extract_text_from_pdf(file_path)
#         # Debug print: show first 300 characters
#         print(f"--- {file_name} ---")
#         print(resume_text[:300])
#         print("\n")
#         resume_embedding = get_embedding(resume_text)
#         score = get_similarity_score(jd_embedding, resume_embedding)
#         results.append((file_name, score))

#     results.sort(key=lambda x: x[1], reverse=True)

#     st.subheader("📊 Ranked Resumes")
#     for name, score in results:
#         st.write(f"**{name}** — Match Score: `{score:.2f}`")
import streamlit as st
import os
from utils.parser import extract_text_from_pdf
from utils.embedder import get_embedding, get_similarity_score

st.title("🔍 Resume Matcher")

# --- Upload Resumes ---
uploaded_files = st.file_uploader(
    "📤 Upload PDF Resumes", type=["pdf"], accept_multiple_files=True
)

# Save uploaded resumes to the /resumes folder
uploaded_file_names = []
if uploaded_files:
    import os
    os.makedirs("resumes", exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = f"resumes/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        uploaded_file_names.append(uploaded_file.name)
    st.success(f"✅ Uploaded {len(uploaded_files)} resume(s) to /resumes")

jd_text = st.text_area("Paste Job Description Here")

if jd_text:
    jd_embedding = get_embedding(jd_text)

    results = []
    for file_name in uploaded_file_names:
        file_path = os.path.join("resumes", file_name)
        resume_text = extract_text_from_pdf(file_path)
        # Debug print: show first 300 characters
        print(f"--- {file_name} ---")
        print(resume_text[:300])
        print("\n")
        resume_embedding = get_embedding(resume_text)
        score = get_similarity_score(jd_embedding, resume_embedding)
        results.append((file_name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    st.subheader("📊 Ranked Resumes")
    for name, score in results:
        st.write(f"{name}** — Match Score: {score:.2f}")