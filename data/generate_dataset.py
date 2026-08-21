import pandas as pd
import numpy as np

np.random.seed(42)
N = 1000  # number of student records

# ── Career profiles ──────────────────────────────────────────────────────────
# Each career has a "ideal profile" range for each feature.
# Features: cgpa, math, english, science, programming, communication,
#           leadership, creativity, analytical, interest_tech, interest_business,
#           interest_health, interest_law, interest_arts, interest_education

career_profiles = {
    "Software Engineer": dict(
        cgpa=(3.2,5.0), math=(7,10), english=(5,9), science=(6,10),
        programming=(7,10), communication=(4,8), leadership=(4,8),
        creativity=(5,9), analytical=(7,10),
        interest_tech=(7,10), interest_business=(2,6), interest_health=(1,4),
        interest_law=(1,3), interest_arts=(1,5), interest_education=(1,5)),

    "Data Scientist": dict(
        cgpa=(3.3,5.0), math=(8,10), english=(5,9), science=(7,10),
        programming=(6,10), communication=(4,8), leadership=(3,7),
        creativity=(5,9), analytical=(8,10),
        interest_tech=(7,10), interest_business=(3,7), interest_health=(2,5),
        interest_law=(1,3), interest_arts=(1,4), interest_education=(2,5)),

    "Cybersecurity Analyst": dict(
        cgpa=(3.0,5.0), math=(6,10), english=(5,9), science=(6,10),
        programming=(6,10), communication=(4,8), leadership=(4,8),
        creativity=(4,8), analytical=(7,10),
        interest_tech=(7,10), interest_business=(2,6), interest_health=(1,4),
        interest_law=(3,7), interest_arts=(1,4), interest_education=(1,4)),

    "Medical Doctor": dict(
        cgpa=(3.8,5.0), math=(6,10), english=(6,9), science=(8,10),
        programming=(1,4), communication=(6,10), leadership=(5,9),
        creativity=(4,8), analytical=(7,10),
        interest_tech=(2,5), interest_business=(2,5), interest_health=(8,10),
        interest_law=(1,4), interest_arts=(1,4), interest_education=(3,7)),

    "Pharmacist": dict(
        cgpa=(3.5,5.0), math=(6,9), english=(6,9), science=(8,10),
        programming=(1,4), communication=(6,9), leadership=(4,8),
        creativity=(4,7), analytical=(7,10),
        interest_tech=(2,5), interest_business=(4,7), interest_health=(8,10),
        interest_law=(1,4), interest_arts=(1,4), interest_education=(3,7)),

    "Lawyer": dict(
        cgpa=(3.2,5.0), math=(4,8), english=(8,10), science=(4,8),
        programming=(1,4), communication=(8,10), leadership=(7,10),
        creativity=(5,9), analytical=(7,10),
        interest_tech=(1,4), interest_business=(4,8), interest_health=(1,4),
        interest_law=(8,10), interest_arts=(3,7), interest_education=(3,7)),

    "Accountant": dict(
        cgpa=(3.0,5.0), math=(8,10), english=(5,9), science=(5,8),
        programming=(2,6), communication=(5,9), leadership=(5,9),
        creativity=(3,7), analytical=(7,10),
        interest_tech=(2,6), interest_business=(8,10), interest_health=(1,4),
        interest_law=(4,7), interest_arts=(1,4), interest_education=(2,5)),

    "Business Manager": dict(
        cgpa=(3.0,5.0), math=(5,9), english=(6,10), science=(4,8),
        programming=(1,5), communication=(7,10), leadership=(8,10),
        creativity=(6,9), analytical=(6,9),
        interest_tech=(2,6), interest_business=(8,10), interest_health=(1,4),
        interest_law=(3,7), interest_arts=(2,6), interest_education=(2,6)),

    "Mechanical Engineer": dict(
        cgpa=(3.0,5.0), math=(7,10), english=(5,8), science=(7,10),
        programming=(3,7), communication=(4,8), leadership=(4,8),
        creativity=(6,9), analytical=(7,10),
        interest_tech=(7,10), interest_business=(2,6), interest_health=(1,4),
        interest_law=(1,3), interest_arts=(3,7), interest_education=(1,4)),

    "Architect": dict(
        cgpa=(3.0,5.0), math=(6,9), english=(5,9), science=(5,9),
        programming=(2,6), communication=(5,9), leadership=(4,8),
        creativity=(8,10), analytical=(6,9),
        interest_tech=(4,8), interest_business=(2,6), interest_health=(1,4),
        interest_law=(1,3), interest_arts=(7,10), interest_education=(2,5)),

    "Teacher / Educator": dict(
        cgpa=(2.8,4.5), math=(5,9), english=(7,10), science=(5,9),
        programming=(1,5), communication=(8,10), leadership=(6,9),
        creativity=(6,9), analytical=(5,9),
        interest_tech=(2,6), interest_business=(2,5), interest_health=(2,5),
        interest_law=(1,4), interest_arts=(4,8), interest_education=(8,10)),

    "Journalist / Media": dict(
        cgpa=(2.7,4.5), math=(3,7), english=(8,10), science=(3,7),
        programming=(2,6), communication=(8,10), leadership=(5,9),
        creativity=(8,10), analytical=(5,9),
        interest_tech=(2,6), interest_business=(2,6), interest_health=(1,4),
        interest_law=(2,6), interest_arts=(7,10), interest_education=(3,7)),

    "Graphic Designer": dict(
        cgpa=(2.5,4.5), math=(3,7), english=(5,9), science=(3,7),
        programming=(3,7), communication=(5,9), leadership=(3,7),
        creativity=(8,10), analytical=(4,8),
        interest_tech=(4,8), interest_business=(2,6), interest_health=(1,3),
        interest_law=(1,3), interest_arts=(8,10), interest_education=(1,4)),

    "Entrepreneur": dict(
        cgpa=(2.5,5.0), math=(5,9), english=(6,10), science=(4,8),
        programming=(2,7), communication=(7,10), leadership=(8,10),
        creativity=(7,10), analytical=(6,9),
        interest_tech=(3,8), interest_business=(8,10), interest_health=(1,4),
        interest_law=(3,7), interest_arts=(3,7), interest_education=(2,6)),

    "Public Administrator": dict(
        cgpa=(2.8,4.5), math=(4,8), english=(7,10), science=(3,7),
        programming=(1,4), communication=(7,10), leadership=(7,10),
        creativity=(4,8), analytical=(5,9),
        interest_tech=(1,4), interest_business=(5,9), interest_health=(2,5),
        interest_law=(6,10), interest_arts=(2,6), interest_education=(4,8)),
}

features = ["cgpa","math","english","science","programming","communication",
            "leadership","creativity","analytical","interest_tech",
            "interest_business","interest_health","interest_law",
            "interest_arts","interest_education"]

records = []
careers = list(career_profiles.keys())
samples_per_career = N // len(careers)

for career, profile in career_profiles.items():
    for _ in range(samples_per_career):
        row = {}
        for feat in features:
            lo, hi = profile[feat]
            if feat == "cgpa":
                val = round(np.random.uniform(lo, hi), 2)
            else:
                val = int(np.clip(np.random.normal((lo+hi)/2, (hi-lo)/4), lo, hi))
            row[feat] = val
        row["career"] = career
        records.append(row)

df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("/home/claude/career_dataset.csv", index=False)
print(f"Dataset created: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nCareer distribution:")
print(df["career"].value_counts())
print("\nSample rows:")
print(df.head(3).to_string())
