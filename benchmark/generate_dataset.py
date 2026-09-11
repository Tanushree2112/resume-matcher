import os
import random
import pandas as pd

random.seed(42)

SKILLS = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Tableau",
        "Pandas", "NumPy", "Statistics", "Data Visualization", "ETL"
    ],
    "Data Scientist": [
        "Python", "SQL", "Machine Learning", "Statistics",
        "Pandas", "NumPy", "Scikit-learn", "XGBoost",
        "Feature Engineering", "Data Visualization"
    ],
    "ML Engineer": [
        "Python", "Machine Learning", "Scikit-learn", "XGBoost",
        "TensorFlow", "PyTorch", "Deep Learning",
        "Feature Engineering", "AWS", "Docker"
    ],
    "NLP Engineer": [
        "Python", "NLP", "Transformers", "BERT",
        "Hugging Face", "RAG", "FAISS", "LLMs",
        "PyTorch", "LangChain"
    ],
    "Business Analyst": [
        "SQL", "Excel", "Power BI", "Tableau",
        "Statistics", "A/B Testing", "KPIs",
        "Data Analysis", "Forecasting", "Stakeholder Management"
    ]
}

os.makedirs("benchmark/jds", exist_ok=True)
os.makedirs("benchmark/resumes", exist_ok=True)

ground_truth = []

roles = list(SKILLS.keys())

for i in range(100):

    role = random.choice(roles)
    required = random.sample(SKILLS[role], 6)

    jd = f"""Job Title: {role}

We are looking for a candidate with experience in:
{', '.join(required)}

Responsibilities:
- Analyze data and generate actionable insights.
- Build analytical solutions and reports.
- Work with cross-functional stakeholders.
"""

    jd_name = f"JD_{i+1}.txt"

    with open(f"benchmark/jds/{jd_name}", "w") as f:
        f.write(jd)

    # 5 candidates: strong → poor
    levels = [
        ("strong", 6),
        ("good", 5),
        ("moderate", 4),
        ("weak", 2),
        ("poor", 1)
    ]

    for level, skill_count in levels:

        candidate_skills = random.sample(required, skill_count)

        # Add unrelated skills to make the ranking realistic
        other_skills = [
            s for r, ss in SKILLS.items()
            for s in ss if s not in required
        ]

        candidate_skills += random.sample(
            list(set(other_skills)),
            min(2, len(set(other_skills)))
        )

        resume = f"""Candidate Resume

Target Role: {role}

Skills:
{', '.join(candidate_skills)}

Experience:
Worked on projects involving data analysis, problem solving,
and technology-driven business solutions.
"""

        resume_name = f"JD_{i+1}_{level}.txt"

        with open(f"benchmark/resumes/{resume_name}", "w") as f:
            f.write(resume)

        ground_truth.append({
            "jd": jd_name,
            "resume": resume_name,
            "relevance": level
        })


pd.DataFrame(ground_truth).to_csv(
    "benchmark/ground_truth.csv",
    index=False
)

print("===================================")
print("Benchmark dataset generated!")
print("100 Job Descriptions")
print("500 Candidate Resumes")
print("500 JD-Resume comparisons")
print("Ground truth saved")
print("===================================")