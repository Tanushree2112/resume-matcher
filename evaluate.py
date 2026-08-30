import os
import csv

from utils.parser import extract_text_from_pdf
from utils.embedder import get_embedding, get_similarity_score
from utils.skill_matcher import get_skill_match


# --------------------------------------------------
# Evaluation JDs
# --------------------------------------------------

JDS = {

    "backend_engineer_cv.pdf": """
    BACKEND SOFTWARE ENGINEER

    We are hiring a Backend Software Engineer to build scalable
    and reliable server-side systems.

    Responsibilities:
    - Design and develop backend services and REST APIs.
    - Build scalable microservices and reliable data processing systems.
    - Work with relational databases and optimize queries.
    - Implement caching, authentication and performance improvements.
    - Use Docker, Git and cloud services.
    - Participate in system design and debugging.

    Requirements:
    - Strong programming experience with Python, Java or C++.
    - Experience with REST APIs and backend frameworks such as FastAPI or Django.
    - Knowledge of PostgreSQL or MySQL and Redis.
    - Experience with Docker, Git and AWS.
    - Understanding of system design, algorithms and data structures.
    """,

    "data_engineer_cv.pdf": """
    DATA ENGINEER

    We are looking for a Data Engineer to build reliable data pipelines
    and scalable data infrastructure.

    Responsibilities:
    - Develop and maintain ETL and data processing pipelines.
    - Transform and integrate data from multiple sources.
    - Build data warehouses and data lakes.
    - Work with large-scale distributed data systems.
    - Ensure data quality, reliability and availability.
    - Collaborate with analytics and data science teams.

    Requirements:
    - Strong Python and SQL skills.
    - Experience with Spark or PySpark.
    - Knowledge of Airflow and ETL workflows.
    - Experience with cloud platforms such as AWS.
    - Familiarity with data warehousing, data pipelines and databases.
    - Knowledge of Snowflake, Databricks or similar platforms is preferred.
    """,

    "data_scientist_cv.pdf": """
    DATA SCIENTIST

    We are hiring a Data Scientist to develop predictive models
    and generate actionable insights from large datasets.

    Responsibilities:
    - Analyze large datasets to identify trends and business insights.
    - Build and evaluate machine learning models.
    - Perform feature engineering and data preprocessing.
    - Use statistical techniques to support decision making.
    - Communicate model results through data visualizations.
    - Work with cross-functional teams to solve business problems.

    Requirements:
    - Strong Python and SQL skills.
    - Experience with Pandas, NumPy and Scikit-learn.
    - Knowledge of statistics and probability.
    - Experience with regression, classification and tree-based models.
    - Knowledge of machine learning and data analysis.
    - Experience with data visualization using Power BI, Tableau or Python libraries.
    """,

    "ml_engineer_cv.pdf": """
    MACHINE LEARNING ENGINEER

    We are looking for a Machine Learning Engineer to develop,
    train and deploy machine learning systems.

    Responsibilities:
    - Develop and train machine learning models.
    - Perform data preprocessing and feature engineering.
    - Experiment with different algorithms and evaluate model performance.
    - Work with deep learning and NLP applications.
    - Develop reproducible ML pipelines.
    - Deploy and monitor machine learning models.

    Requirements:
    - Strong Python programming skills.
    - Experience with Scikit-learn, PyTorch or TensorFlow.
    - Knowledge of machine learning and deep learning.
    - Experience with neural networks, CNNs, RNNs or LSTMs.
    - Knowledge of NLP and transformer-based models.
    - Familiarity with Docker, Git and cloud platforms.
    - Understanding of model evaluation and experimentation.
    """,

    "business_analyst_cv.pdf": """
    BUSINESS ANALYST

    We are looking for a Business Analyst to support business
    decisions through data-driven analysis.

    Responsibilities:
    - Analyze business and operational data to identify trends.
    - Translate business requirements into analytical problems.
    - Build reports and dashboards for stakeholders.
    - Track KPIs and monitor business performance.
    - Work with cross-functional teams to identify opportunities.
    - Present insights and recommendations to business teams.

    Requirements:
    - Strong analytical and problem-solving skills.
    - Proficiency in SQL and Excel.
    - Experience with Power BI or Tableau.
    - Knowledge of statistics and data visualization.
    - Ability to communicate insights clearly to stakeholders.
    - Experience with KPI analysis, reporting and business metrics.
    """,

    "product_analyst_cv.pdf": """
    PRODUCT ANALYST

    We are hiring a Product Analyst to use data to understand
    user behavior and improve product performance.

    Responsibilities:
    - Analyze product and user behavior data.
    - Define and monitor product KPIs.
    - Build dashboards and reports for product teams.
    - Analyze funnels, cohorts and user retention.
    - Conduct A/B testing and evaluate product experiments.
    - Generate insights to improve user engagement and conversion.
    - Work closely with Product Managers and business teams.

    Requirements:
    - Strong SQL and Python skills.
    - Experience with product analytics and data visualization.
    - Knowledge of KPIs, funnels, cohorts, retention and churn.
    - Understanding of A/B testing and experimentation.
    - Strong analytical and communication skills.
    - Experience with tools such as Excel, Tableau or Power BI is preferred.
    """
}


# --------------------------------------------------
# Load resumes
# --------------------------------------------------

resume_folder = "resumes"

resume_files = [
    file for file in os.listdir(resume_folder)
    if file.lower().endswith(".pdf")
]


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

evaluation_rows = []
results = []

for correct_resume, jd_text in JDS.items():

    print("\n" + "=" * 60)
    print(f"JD: {correct_resume}")
    print("=" * 60)

    jd_embedding = get_embedding(jd_text)

    rankings = []

    for resume_file in resume_files:

        resume_path = os.path.join(
            resume_folder,
            resume_file
        )

        resume_text = extract_text_from_pdf(resume_path)

        # Semantic similarity
        resume_embedding = get_embedding(resume_text)

        semantic_score = get_similarity_score(
            jd_embedding,
            resume_embedding
        )

        # Skill score
        skill_score, matched, missing = get_skill_match(
            jd_text,
            resume_text
        )

        # Same scoring used by app.py
        final_score = (
            0.7 * semantic_score
            + 0.3 * skill_score
        )

        rankings.append(
            (resume_file, final_score)
        )

    # Highest score first
    rankings.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Display ranking
    for rank, (resume_file, score) in enumerate(
        rankings,
        start=1
    ):
        print(
            f"{rank}. {resume_file:<30} "
            f"{score:.3f}"
        )

    # Find correct resume rank
    correct_rank = next(
        rank
        for rank, (resume_file, _) in enumerate(
            rankings,
            start=1
        )
        if resume_file == correct_resume
    )

    evaluation_rows.append({
    "JD": correct_resume,
    "Correct_Rank": correct_rank,
    "Top_1": correct_rank == 1,
    "Top_3": correct_rank <= 3
})

    results.append(correct_rank)

    print(
        f"\nCorrect resume rank: #{correct_rank}"
    )


# --------------------------------------------------
# Evaluation Metrics
# --------------------------------------------------

total = len(results)

top_1 = sum(
    rank <= 1
    for rank in results
) / total

top_3 = sum(
    rank <= 3
    for rank in results
) / total

mrr = sum(
    1 / rank
    for rank in results
) / total


print("\n")
print("=" * 60)
print("FINAL EVALUATION")
print("=" * 60)

print(f"Total JDs tested : {total}")
print(f"Top-1 Accuracy   : {top_1:.2%}")
print(f"Top-3 Accuracy   : {top_3:.2%}")
print(f"MRR              : {mrr:.3f}")

print("=" * 60)

# Save evaluation results
with open(
    "evaluation_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "JD",
            "Correct_Rank",
            "Top_1",
            "Top_3"
        ]
    )

    writer.writeheader()
    writer.writerows(evaluation_rows)

print("\nEvaluation results saved to evaluation_results.csv")