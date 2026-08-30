# SkillAlign — NLP Resume-to-JD Matching System

SkillAlign is an NLP-based resume screening and ranking system that matches multiple candidate resumes against a job description and ranks candidates based on semantic similarity and required skill overlap.

## Problem

Recruiters often need to screen large numbers of resumes against a job description. Keyword-only matching can miss semantic relationships between skills and job requirements.

SkillAlign combines **Sentence-BERT semantic embeddings** with **skill-based matching** to produce a more meaningful candidate ranking.

## Key Features

- Upload multiple candidate resumes in PDF format
- Upload a Job Description as a PDF or paste it directly
- Extract resume text using `pdfplumber`
- Extract and normalize technical skills
- Handle common skill aliases such as:
  - `postgres` → `postgresql`
  - `fast api` → `fastapi`
  - `restful api` → `rest api`
  - `py spark` → `pyspark`
  - `c plus plus` → `c++`
- Generate Sentence-BERT embeddings using `all-MiniLM-L6-v2`
- Calculate cosine similarity between resume and JD embeddings
- Calculate skill-match percentage
- Combine semantic and skill scores into an overall match score
- Rank candidates from highest to lowest match
- Display matched and missing/weak skills
- Generate recruiter-style explanations for candidate rankings
- Evaluate ranking performance using Top-K accuracy and MRR

## System Pipeline

Candidate Resumes (PDF)
        |
        v
PDF Text Extraction
    (pdfplumber)
        |
        v
Skill Extraction
   + Normalization
        |
        +--------------------+
        |                    |
        v                    v
Sentence-BERT          Skill Matching
Embeddings             & Skill Score
        |                    |
        v                    v
Cosine Similarity       Skill Match %
        |                    |
        +---------+----------+
                  |
                  v
         Weighted Match Score
                  |
                  v
         Candidate Ranking
                  |
                  v
      Matched / Missing Skills
             + Explanation

## Matching Method

Each resume and job description is converted into a dense vector representation using:

**Sentence-BERT — `all-MiniLM-L6-v2`**

Cosine similarity is then used to measure semantic alignment between the resume and job description.

The system also extracts required skills from the job description and candidate resume.

### Skill Match

Skill Match is calculated as:

`Matched JD Skills / Total JD Skills`

This captures explicit overlap between the candidate's skills and the skills required by the job.

### Overall Match

The final score combines:

- Semantic similarity
- Skill match

This allows the system to consider both **contextual similarity** and **explicit technical skill overlap** when ranking candidates.

## Skill Normalization

The skill extraction pipeline normalizes common variations before comparison.

Examples:

- `Postgres` → `PostgreSQL`
- `Fast API` → `FastAPI`
- `RESTful API` → `REST API`
- `Py Spark` → `PySpark`
- `C plus plus` → `C++`

This reduces false negatives caused by different ways of writing the same skill.

## Evaluation

The ranking pipeline was evaluated on **6 labeled job descriptions** covering different profiles:

- Backend Software Engineer
- Data Engineer
- Data Scientist
- Machine Learning Engineer
- Business Analyst
- Product Analyst

The correct/reference resume was ranked **#1 for all 6 job descriptions**.

| Metric | Result |
|---|---:|
| Top-1 Accuracy | 100% |
| Top-3 Accuracy | 100% |
| MRR | 1.00 |

The evaluation dataset is intentionally small and should be treated as a validation benchmark rather than evidence of 100% real-world accuracy. A larger human-labeled dataset would be required to evaluate production-level performance.

## Tech Stack

- Python
- Streamlit
- Sentence-Transformers
- Scikit-learn
- PyTorch
- pdfplumber
- Pandas

## Project Structure

skill_align/
|
├── app.py
├── evaluate.py
├── evaluation_results.csv
├── requirements.txt
├── README.md
├── .gitignore
|
├── utils/
│   ├── parser.py
│   ├── embedder.py
│   └── skill_matcher.py
|
├── job_descriptions/
└── resumes/

## Installation

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

## How It Works

1. Upload multiple candidate resumes in PDF format.
2. Upload a Job Description PDF or paste the JD manually.
3. The system extracts text from the uploaded documents using `pdfplumber`.
4. Required skills are extracted and normalized using predefined skill aliases.
5. Resume and JD text are converted into embeddings using Sentence-BERT (`all-MiniLM-L6-v2`).
6. Cosine similarity measures semantic alignment between each resume and the JD.
7. Explicit skill overlap is calculated separately.
8. Semantic similarity and skill match are combined into an overall match score.
9. Candidates are ranked from highest to lowest score.
10. The interface displays matched skills, missing/weak skills, and an explanation for each candidate.

## Evaluation

The project includes a separate evaluation script to test whether the correct resume is ranked highly for known job descriptions.

Run:

python evaluate.py

The evaluation results are saved to:

evaluation_results.csv

The benchmark contains 6 job descriptions covering:

- Backend Software Engineer
- Data Engineer
- Data Scientist
- Machine Learning Engineer
- Business Analyst
- Product Analyst

### Evaluation Results

| Metric | Result |
|---|---:|
| Top-1 Accuracy | 100% |
| Top-3 Accuracy | 100% |
| Mean Reciprocal Rank (MRR) | 1.00 |

The correct/reference resume was ranked #1 for all 6 benchmark job descriptions.

**Important:** These results are based on a small validation benchmark and should not be interpreted as 100% real-world accuracy. A larger human-labeled dataset would be required for robust evaluation.

## Example Output

For each candidate, the system displays:

- Overall Match Score
- Semantic Similarity
- Skill Match
- Matched Skills
- Missing / Weak Skills
- Candidate Match Explanation

Example:

Overall Match: 84%

Semantic Similarity: 0.84

Skill Match: 82%

Matched Skills: Python, SQL, AWS, ETL, Airflow, Spark

Missing / Weak Skills: Snowflake, Databricks

## Project Structure

skill_align/
│
├── app.py
├── evaluate.py
├── evaluation_results.csv
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── parser.py
│   ├── embedder.py
│   ├── skill_matcher.py
│   └── llm_feedback.py
│
├── job_descriptions/
└── resumes/

## Technology Stack

- Python
- Streamlit
- Sentence-Transformers
- Sentence-BERT
- Scikit-learn
- PyTorch
- pdfplumber
- Pandas
- OpenAI API (optional recruiter-feedback feature)

## Future Improvements

- Expand the evaluation dataset with hundreds of labeled resumes and JDs
- Improve the skill taxonomy and alias mapping
- Add section-aware resume parsing
- Match experience, education, and seniority requirements
- Add Precision@K, Recall@K and NDCG evaluation
- Add recruiter feedback and explainable recommendations
- Support batch candidate screening and CSV export
- Use a vector database for large-scale candidate retrieval

## Limitations

- Resume parsing depends on the quality and structure of the PDF.
- Skill matching currently relies on a predefined skill dictionary.
- Semantic similarity does not guarantee that a candidate actually satisfies every job requirement.
- The current evaluation dataset is small.
- The system is designed as a screening aid and not as an autonomous hiring decision system.

## Disclaimer

SkillAlign is a resume screening and ranking tool designed to assist recruiters and candidates. Final hiring decisions should always involve human evaluation.