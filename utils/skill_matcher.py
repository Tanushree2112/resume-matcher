import re

# Skills relevant to common Data / ML / Software roles
SKILLS = [
    # Programming
    "python", "java", "c++", "javascript", "sql",

    # Data
    "excel", "power bi", "tableau", "pandas", "numpy",
    "scikit-learn", "statistics", "data analysis",
    "data visualization", "a/b testing",

    # ML / AI
    "machine learning", "deep learning", "nlp",
    "xgboost", "random forest", "logistic regression",
    "linear regression", "tensorflow", "pytorch",
    "transformers", "bert", "rag", "llm",
    "computer vision", "k-means", "pca",

    # Data Engineering
    "spark", "pyspark", "airflow", "etl",
    "data pipelines", "data warehousing",

    # Backend / Software
    "fastapi", "django", "rest api", "postgresql",
    "mysql", "redis", "docker", "git", "aws",
    "microservices", "system design",
    "data structures", "algorithms",

    # Product / Analytics
    "product analytics", "kpi", "funnel analysis",
    "cohort analysis", "retention", "churn"
]

SKILL_ALIASES = {
    # Databases
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "mysql": "mysql",
    "sql server": "sql",

    # APIs / Backend
    "rest apis": "rest api",
    "rest api": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "fast api": "fastapi",
    "fastapi": "fastapi",

    # ML / AI
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",

    "tf": "tensorflow",
    "tensorflow": "tensorflow",

    "torch": "pytorch",
    "pytorch": "pytorch",

    # Data
    "powerbi": "power bi",
    "power bi": "power bi",

    # NLP
    "sentence bert": "bert",
    "sentence-bert": "bert",

    # Cloud
    "amazon web services": "aws",
    "aws": "aws",

    # Data Engineering
    "py spark": "pyspark",
    "py-spark": "pyspark",
    "pyspark": "pyspark",

    # Programming
    "c plus plus": "c++",
    "c++": "c++",
}

# Common technical terms that may appear in JDs
# but are not necessarily part of our main SKILLS list.
TECHNICAL_TERMS = [
    "snowflake", "databricks", "dbt", "kafka", "hadoop",
    "looker", "sas", "r", "azure", "gcp",
    "bigquery", "redshift", "athena",
    "mongodb", "oracle", "sqlite",
    "hive", "presto", "trino",
    "flink", "kubernetes", "jenkins",
    "terraform", "ansible",
    "spark sql", "data lake", "data lakehouse",
    "delta lake", "mlflow",
    "streamlit", "langchain",
    "openai", "hugging face",
    "gitlab", "bitbucket"
]

def normalize_text(text):
    """
    Normalize text before skill extraction.
    Converts different spellings of the same skill
    into a common canonical form.
    """

    text = text.lower()

    # Normalize common punctuation variations
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Apply aliases
    # Longer aliases first to avoid partial replacements
    for alias, canonical in sorted(
        SKILL_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        text = re.sub(pattern, canonical, text)

    return text

def extract_skills(text):
    """
    Extract normalized skills from text.
    """

    text = normalize_text(text)

    found_skills = set()

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)

def extract_dynamic_skills(text):
    """
    Detect additional technical terms that may not be
    present in the main SKILLS list.
    """

    text = normalize_text(text)

    found_skills = set()

    for skill in TECHNICAL_TERMS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)

def extract_required_preferred_skills(jd_text):
    """
    Separate JD skills into required and preferred skills
    based on common section headings.
    """

    jd_text = normalize_text(jd_text)

    required_skills = set()
    preferred_skills = set()

    # Split JD into sections
    required_section = jd_text
    preferred_section = ""

    preferred_markers = [
        "preferred:",
        "preferred skills:",
        "nice to have:",
        "nice-to-have:",
        "bonus:",
        "preferred qualifications:"
    ]

    for marker in preferred_markers:
        if marker in jd_text:
            parts = jd_text.split(marker, 1)
            required_section = parts[0]
            preferred_section = parts[1]
            break

    # Extract known + additional technical skills
    required_skills = (
        set(extract_skills(required_section))
        | set(extract_dynamic_skills(required_section))
    )

    preferred_skills = (
        set(extract_skills(preferred_section))
        | set(extract_dynamic_skills(preferred_section))
    )

    # A preferred skill should not also be required
    preferred_skills -= required_skills

    return required_skills, preferred_skills    

def get_skill_match(jd_text, resume_text):
    """
    Compare required and preferred skills between
    JD and resume.
    """

    required_skills, preferred_skills = (
        extract_required_preferred_skills(jd_text)
    )

    resume_skills = (
        set(extract_skills(resume_text))
        | set(extract_dynamic_skills(resume_text))
    )

    # Required skills
    matched_required = sorted(
        required_skills & resume_skills
    )

    missing_required = sorted(
        required_skills - resume_skills
    )

    # Preferred skills
    matched_preferred = sorted(
        preferred_skills & resume_skills
    )

    missing_preferred = sorted(
        preferred_skills - resume_skills
    )

    # Calculate scores
    if required_skills:
        required_score = (
            len(matched_required) /
            len(required_skills)
        )
    else:
        required_score = 0

    if preferred_skills:
        preferred_score = (
            len(matched_preferred) /
            len(preferred_skills)
        )
    else:
        preferred_score = 0

    # Required skills matter more
    if required_skills and preferred_skills:
        skill_score = (
            0.75 * required_score
            + 0.25 * preferred_score
        )
    elif required_skills:
        skill_score = required_score
    else:
        skill_score = preferred_score

    matched = sorted(
        matched_required + matched_preferred
    )

    missing = sorted(
        missing_required + missing_preferred
    )

    return (
        skill_score,
        matched,
        missing
    )

def generate_match_explanation(
    semantic_score,
    skill_score,
    matched_skills,
    missing_skills
):
    """
    Generate a simple explanation for why a resume
    received its match score.
    """

    explanation = []

    # Semantic alignment
    if semantic_score >= 0.70:
        explanation.append(
            "Strong semantic alignment with the job description."
        )
    elif semantic_score >= 0.50:
        explanation.append(
            "Moderate semantic alignment with the job description."
        )
    else:
        explanation.append(
            "Limited semantic alignment with the job description."
        )

    # Skill alignment
    if skill_score >= 0.75:
        explanation.append(
            "The resume covers most of the identified job skills."
        )
    elif skill_score >= 0.40:
        explanation.append(
            "The resume covers several relevant job skills."
        )
    else:
        explanation.append(
            "The resume has limited overlap with the required skills."
        )

    # Missing skills
    if missing_skills:
        explanation.append(
            "Key missing or weak skills: "
            + ", ".join(missing_skills[:5])
            + "."
        )

    return " ".join(explanation)