import streamlit as st
import os
import pandas as pd

from utils.parser import extract_text_from_pdf
from utils.embedder import get_embedding, get_similarity_score
from utils.skill_matcher import (
    get_skill_match,
    generate_match_explanation
)


st.title("Resume Matcher")

# -----------------------------
# Upload Resumes
# -----------------------------

uploaded_files = st.file_uploader(
    "Upload PDF Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

uploaded_file_names = []

if uploaded_files:

    os.makedirs("resumes", exist_ok=True)

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            "resumes",
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        uploaded_file_names.append(uploaded_file.name)

    st.success(
        f"Uploaded {len(uploaded_files)} resume(s) to /resumes"
    )


# -----------------------------
# Job Description
# -----------------------------

st.subheader("Job Description")

jd_file = st.file_uploader(
    "Upload Job Description PDF (optional)",
    type=["pdf"],
    accept_multiple_files=False
)

jd_text = st.text_area(
    "Or paste Job Description here",
    height=200
)

if jd_file:
    os.makedirs("job_descriptions", exist_ok=True)

    jd_path = os.path.join(
        "job_descriptions",
        jd_file.name
    )

    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())

    jd_text = extract_text_from_pdf(jd_path)

    st.success(
        f"Loaded Job Description: {jd_file.name}"
    )


# -----------------------------
# Matching
# -----------------------------

if jd_text and uploaded_file_names:

    jd_embedding = get_embedding(jd_text)

    results = []

    for file_name in uploaded_file_names:

        file_path = os.path.join(
            "resumes",
            file_name
        )

        # Extract resume text
        resume_text = extract_text_from_pdf(file_path)

        # SBERT similarity
        resume_embedding = get_embedding(resume_text)

        semantic_score = get_similarity_score(
            jd_embedding,
            resume_embedding
        )

        # Skill matching
        skill_score, matched_skills, missing_skills = get_skill_match(
            jd_text,
            resume_text
        )

        explanation = generate_match_explanation(
            semantic_score,
            skill_score,
            matched_skills,
            missing_skills
        )

        # Weighted final score
        final_score = (
            0.7 * semantic_score
            + 0.3 * skill_score
        )

        results.append({
            "name": file_name,
            "score": final_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "matched": matched_skills,
            "missing": missing_skills,
            "explanation": explanation
        })


    # Sort highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # -----------------------------
    # Display Results
    # -----------------------------

    st.subheader("Ranked Resumes")

    for i, result in enumerate(results):

        st.write(
            f"### {i + 1}. {result['name']}"
        )

        st.write(
            f"**Overall Match: "
            f"{result['score']:.0%}**"
        )

        st.write(
            f"Semantic Similarity: "
            f"{result['semantic_score']:.2f}"
        )

        st.write(
            f"Skill Match: "
            f"{result['skill_score']:.0%}"
        )

        if result["matched"]:

            st.write(
                "**Matched Skills:** "
                + ", ".join(result["matched"])
            )

        if result["missing"]:

            st.write(
                "**Missing / Weak Skills:** "
                + ", ".join(result["missing"])
            )

        st.write(
            "**Why this candidate matches:** "
            + result["explanation"]
        )

        st.divider()

st.subheader("Model Evaluation")

if os.path.exists("evaluation_results.csv"):
    eval_df = pd.read_csv("evaluation_results.csv")

    top1 = eval_df["Top_1"].mean()
    top3 = eval_df["Top_3"].mean()
    mrr = (
        1 / eval_df["Correct_Rank"]
    ).mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Top-1 Accuracy", f"{top1:.0%}")
    col2.metric("Top-3 Accuracy", f"{top3:.0%}")
    col3.metric("MRR", f"{mrr:.3f}")

    st.caption(
        f"Evaluated on {len(eval_df)} job descriptions"
    )