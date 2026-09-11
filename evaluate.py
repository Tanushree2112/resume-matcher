import os
import pandas as pd

from utils.embedder import get_embedding, get_similarity_score
from utils.skill_matcher import get_skill_match


# --------------------------------------------------
# Benchmark paths
# --------------------------------------------------

JD_FOLDER = "benchmark/jds"
RESUME_FOLDER = "benchmark/resumes"
GROUND_TRUTH = "benchmark/ground_truth.csv"


# --------------------------------------------------
# Load ground truth
# --------------------------------------------------

ground_truth = pd.read_csv(GROUND_TRUTH)

results = []


# --------------------------------------------------
# Evaluate each JD
# --------------------------------------------------

for jd_file in sorted(os.listdir(JD_FOLDER)):

    if not jd_file.endswith(".txt"):
        continue

    jd_path = os.path.join(JD_FOLDER, jd_file)

    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_embedding = get_embedding(jd_text)

    # Get resumes belonging to this JD
    jd_data = ground_truth[
        ground_truth["jd"] == jd_file
    ]

    rankings = []

    for _, row in jd_data.iterrows():

        resume_file = row["resume"]
        resume_path = os.path.join(
            RESUME_FOLDER,
            resume_file
        )

        with open(resume_path, "r", encoding="utf-8") as f:
            resume_text = f.read()

        # ------------------------------------------
        # Semantic similarity
        # ------------------------------------------

        resume_embedding = get_embedding(resume_text)

        semantic_score = get_similarity_score(
            jd_embedding,
            resume_embedding
        )

        # ------------------------------------------
        # Explicit skill matching
        # ------------------------------------------

        skill_score, matched, missing = get_skill_match(
            jd_text,
            resume_text
        )

        # ------------------------------------------
        # Hybrid score
        # ------------------------------------------

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

    # ------------------------------------------------
    # Ground-truth best resume = "strong"
    # ------------------------------------------------

    correct_resume = jd_data[
        jd_data["relevance"] == "strong"
    ]["resume"].iloc[0]

    correct_rank = next(
        rank
        for rank, (resume_file, _) in enumerate(
            rankings,
            start=1
        )
        if resume_file == correct_resume
    )

    results.append({
        "JD": jd_file,
        "Correct_Resume": correct_resume,
        "Correct_Rank": correct_rank,
        "Top_1": correct_rank == 1,
        "Top_3": correct_rank <= 3
    })

    # Progress
    print(
        f"{jd_file}: Correct rank = #{correct_rank}"
    )


# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

df = pd.DataFrame(results)

total = len(df)

top_1 = df["Top_1"].mean()
top_3 = df["Top_3"].mean()

mrr = (
    1 / df["Correct_Rank"]
).mean()


# --------------------------------------------------
# Final results
# --------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL BENCHMARK EVALUATION")
print("=" * 60)

print(f"Total JDs tested : {total}")
print(f"Total comparisons: {total * 5}")

print(f"Top-1 Hit Rate   : {top_1:.2%}")
print(f"Top-3 Hit Rate   : {top_3:.2%}")
print(f"MRR              : {mrr:.3f}")

print("=" * 60)


# --------------------------------------------------
# Save results
# --------------------------------------------------

df.to_csv(
    "benchmark/evaluation_results.csv",
    index=False
)

print(
    "\nResults saved to "
    "benchmark/evaluation_results.csv"
)