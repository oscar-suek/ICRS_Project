"""
ICRS — Stage 1: Model Training
Intelligent Career Recommendation System
University of Benin Final Year Project
"""

import pandas as pd
import numpy as np
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── 1. LOAD DATA ─────────────────────────────────────────────────────────────
print("=" * 60)
print("  ICRS — Intelligent Career Recommendation System")
print("  Model Training Script")
print("=" * 60)

df = pd.read_csv("/home/claude/career_dataset.csv")
print(f"\n[1] Dataset loaded: {df.shape[0]} records, {df.shape[1]} columns")
print(f"    Careers: {df['career'].nunique()} unique career labels")
print(f"    Missing values: {df.isnull().sum().sum()}")

# ── 2. FEATURE / LABEL SPLIT ──────────────────────────────────────────────────
features = ["cgpa","math","english","science","programming","communication",
            "leadership","creativity","analytical","interest_tech",
            "interest_business","interest_health","interest_law",
            "interest_arts","interest_education"]

X = df[features]
y = df["career"]

# ── 3. ENCODE LABELS ──────────────────────────────────────────────────────────
le = LabelEncoder()
y_encoded = le.fit_transform(y)
print(f"\n[2] Label encoding complete.")
print(f"    Classes: {list(le.classes_)}")

# ── 4. TRAIN/TEST SPLIT ───────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
print(f"\n[3] Train/Test split: {len(X_train)} train / {len(X_test)} test")

# ── 5. SCALE FEATURES ─────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 6. TRAIN & COMPARE CLASSIFIERS ───────────────────────────────────────────
print("\n[4] Training and comparing classifiers...")
print("-" * 45)

classifiers = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    "k-NN":          KNeighborsClassifier(n_neighbors=5),
    "SVM":           SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42),
    "Naive Bayes":   GaussianNB(),
}

results = {}
for name, clf in classifiers.items():
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    cv  = cross_val_score(clf, X_train_scaled, y_train, cv=5, scoring="accuracy")
    results[name] = {"accuracy": acc, "cv_mean": cv.mean(), "cv_std": cv.std()}
    print(f"  {name:<20} Test Acc: {acc*100:.2f}%   CV: {cv.mean()*100:.2f}% ± {cv.std()*100:.2f}%")

print("-" * 45)
best_name = max(results, key=lambda k: results[k]["accuracy"])
print(f"  Best classifier: {best_name} ({results[best_name]['accuracy']*100:.2f}%)")

# ── 7. DETAILED EVALUATION OF RANDOM FOREST ──────────────────────────────────
rf = classifiers["Random Forest"]
y_pred_rf = rf.predict(X_test_scaled)

print(f"\n[5] Random Forest — Detailed Evaluation")
print("-" * 45)
print(classification_report(y_test, y_pred_rf, target_names=le.classes_))

# ── 8. CONFUSION MATRIX ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 11))
cm = confusion_matrix(y_test, y_pred_rf)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(ax=ax, xticks_rotation=45, colorbar=True, cmap="Blues")
ax.set_title("ICRS — Random Forest Confusion Matrix", fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("/home/claude/confusion_matrix.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n[6] Confusion matrix saved.")

# ── 9. FEATURE IMPORTANCE ─────────────────────────────────────────────────────
importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 7))
colors = ["#2196F3" if v > importances.mean() else "#90CAF9" for v in importances]
importances.plot(kind="barh", ax=ax, color=colors)
ax.set_title("ICRS — Feature Importance (Random Forest)", fontsize=13, fontweight="bold")
ax.set_xlabel("Importance Score")
ax.axvline(importances.mean(), color="red", linestyle="--", linewidth=1, label="Mean importance")
ax.legend()
plt.tight_layout()
plt.savefig("/home/claude/feature_importance.png", dpi=150, bbox_inches="tight")
plt.close()
print("[7] Feature importance chart saved.")

# ── 10. CLASSIFIER COMPARISON CHART ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
names = list(results.keys())
accs  = [results[n]["accuracy"] * 100 for n in names]
colors_bar = ["#1565C0" if n == best_name else "#90CAF9" for n in names]
bars = ax.bar(names, accs, color=colors_bar, width=0.5)
ax.set_ylim(50, 105)
ax.set_ylabel("Test Accuracy (%)")
ax.set_title("ICRS — Classifier Comparison", fontsize=13, fontweight="bold")
for bar, acc in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{acc:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
plt.tight_layout()
plt.savefig("/home/claude/classifier_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("[8] Classifier comparison chart saved.")

# ── 11. SAVE MODEL ARTIFACTS ──────────────────────────────────────────────────
joblib.dump(rf,     "/home/claude/model.pkl")
joblib.dump(le,     "/home/claude/label_encoder.pkl")
joblib.dump(scaler, "/home/claude/scaler.pkl")

# Save feature list and career labels as JSON (needed by Flask)
meta = {
    "features": features,
    "careers":  list(le.classes_),
    "accuracy": round(results["Random Forest"]["accuracy"] * 100, 2)
}
with open("/home/claude/model_meta.json", "w") as f:
    json.dump(meta, f, indent=2)

print("\n[9] Model artifacts saved:")
print("    model.pkl          — trained Random Forest model")
print("    label_encoder.pkl  — career label encoder")
print("    scaler.pkl         — feature scaler")
print("    model_meta.json    — feature list & career labels")

# ── 12. QUICK PREDICTION TEST ─────────────────────────────────────────────────
print("\n[10] Quick prediction test:")
sample = pd.DataFrame([{
    "cgpa": 4.2, "math": 9, "english": 6, "science": 8,
    "programming": 8, "communication": 6, "leadership": 5,
    "creativity": 6, "analytical": 9, "interest_tech": 9,
    "interest_business": 3, "interest_health": 2, "interest_law": 1,
    "interest_arts": 3, "interest_education": 2
}])
sample_scaled = scaler.transform(sample)
pred_label    = le.inverse_transform(rf.predict(sample_scaled))[0]
pred_proba    = rf.predict_proba(sample_scaled)[0]
top3_idx      = pred_proba.argsort()[-3:][::-1]
print(f"    Student: High CGPA, strong math/programming, loves tech")
print(f"    Top 3 Recommendations:")
for i, idx in enumerate(top3_idx, 1):
    print(f"      {i}. {le.classes_[idx]:<25} ({pred_proba[idx]*100:.1f}% confidence)")

print("\n" + "=" * 60)
print("  Stage 1 Complete — Model ready for Flask integration")
print("=" * 60)
