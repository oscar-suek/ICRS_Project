"""
Intelligent Career Recommendation System (ICRS) — Stage 2
Flask backend that serves predictions from the trained Random Forest model.

Expects these files inside ./models/  (copy your Stage 1 outputs here):
    model.pkl
    label_encoder.pkl
    scaler.pkl
    model_meta.json
    career_dataset.csv   (optional at runtime — only needed if you want /retrain or stats)
"""

import csv
import json
import os
import traceback
from datetime import datetime, timezone

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app.py lives in ICRS_Project/app/, and the trained model files live in
# ICRS_Project/model/ (a sibling folder) — so go one level up.
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# On Vercel, files in ICRS_Project/public/ are served automatically by the
# CDN — this constant + route below only exist so the same /style.css and
# /script.js paths also work when running locally with `python app.py`.
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
MODEL_DIR = os.path.join(PROJECT_ROOT, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
META_PATH = os.path.join(MODEL_DIR, "model_meta.json")

# Every /predict call gets appended here — inputs, result, timestamp.
LOG_DIR = os.path.join(PROJECT_ROOT, "data")
LOG_PATH = os.path.join(LOG_DIR, "prediction_log.csv")

# Below this top-prediction confidence (%), the response flags the result as
# low-confidence instead of presenting it as a firm recommendation.
CONFIDENCE_THRESHOLD = 40

# Canonical feature order — used as a fallback if model_meta.json doesn't
# specify one. IMPORTANT: this must match the exact column order the model
# was trained on.
DEFAULT_FEATURE_ORDER = [
    "cgpa",
    "math",
    "english",
    "science",
    "programming",
    "communication",
    "leadership",
    "creativity",
    "analytical",
    "interest_tech",
    "interest_business",
    "interest_health",
    "interest_law",
    "interest_arts",
    "interest_education",
]

# Short, plain-language explanation of each field, shown in the intro modal.
FIELD_DESCRIPTIONS = {
    "cgpa": "Your current cumulative grade point average.",
    "math": "How strong your math skills are.",
    "english": "How strong your English/communication-in-writing skills are.",
    "science": "How strong your general science skills are.",
    "programming": "How comfortable you are writing and reasoning about code.",
    "communication": "How well you express ideas and work with others verbally.",
    "leadership": "How comfortable you are guiding or coordinating a team.",
    "creativity": "How much you enjoy generating new ideas or original work.",
    "analytical": "How strong your logical and problem-solving skills are.",
    "interest_tech": "How interested you are in technology and computing.",
    "interest_business": "How interested you are in business, finance, or management.",
    "interest_health": "How interested you are in health, medicine, or wellbeing careers.",
    "interest_law": "How interested you are in law, justice, or policy.",
    "interest_arts": "How interested you are in creative arts or design.",
    "interest_education": "How interested you are in teaching or education.",
}

app = Flask(__name__)
CORS(app)  # allow the HTML/CSS/JS frontend to call this API from another origin/port

# --------------------------------------------------------------------------
# Load model artifacts once at startup
# --------------------------------------------------------------------------

model = None
label_encoder = None
scaler = None
model_meta = {}
feature_order = DEFAULT_FEATURE_ORDER


def load_artifacts():
    global model, label_encoder, scaler, model_meta, feature_order

    missing = [
        p
        for p in [MODEL_PATH, ENCODER_PATH, SCALER_PATH, META_PATH]
        if not os.path.exists(p)
    ]
    if missing:
        raise FileNotFoundError(
            "Missing model artifact(s): "
            + ", ".join(missing)
            + f"\nPlace your Stage 1 files inside: {MODEL_DIR}"
        )

    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)

    with open(META_PATH, "r") as f:
        model_meta = json.load(f)

    # Use feature order from metadata if present, otherwise fall back to default
    feature_order = model_meta.get("feature_names", DEFAULT_FEATURE_ORDER)

    print(f"[ICRS] Model loaded. Accuracy: {model_meta.get('accuracy', 'N/A')}")
    print(f"[ICRS] Feature order: {feature_order}")
    print(f"[ICRS] Classes: {list(label_encoder.classes_)}")


try:
    load_artifacts()
except FileNotFoundError as e:
    # App still starts so you can hit / and see setup instructions,
    # but /predict will return a clear 503 until files are in place.
    print(f"[ICRS] WARNING: {e}")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

VALID_RANGES = {
    "cgpa": (0.0, 5.0),  # adjust to your school's grading scale (e.g. 0-4 or 0-5)
}
DEFAULT_SCORE_RANGE = (0, 10)  # skill/interest ratings are on a 0-10 scale


def validate_and_extract(payload: dict):
    """Validate incoming JSON and return an ordered feature vector, or raise ValueError."""
    missing_fields = [f for f in feature_order if f not in payload]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    vector = []
    for field in feature_order:
        value = payload[field]
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Field '{field}' must be numeric, got: {value!r}")

        lo, hi = VALID_RANGES.get(field, DEFAULT_SCORE_RANGE)
        if not (lo <= value <= hi):
            raise ValueError(f"Field '{field}' must be between {lo} and {hi}, got: {value}")

        vector.append(value)

    return np.array(vector).reshape(1, -1)


def model_ready():
    return all(x is not None for x in (model, label_encoder, scaler))


def get_field_ranges():
    """Return {field_name: (min, max)} for every field, for use in the HTML form.
    Pulls from VALID_RANGES first, falls back to DEFAULT_SCORE_RANGE — so the
    form always matches whatever validate_and_extract() actually enforces."""
    return {f: VALID_RANGES.get(f, DEFAULT_SCORE_RANGE) for f in feature_order}


def pretty_label(field: str) -> str:
    """Turn a raw feature name into a human-readable form field label."""
    if field == "cgpa":
        return "CGPA"
    if field.startswith("interest_"):
        topic = field[len("interest_"):].replace("_", " ").title()
        return f"Interest in {topic}"
    return field.replace("_", " ").title()


def get_field_labels():
    return {f: pretty_label(f) for f in feature_order}


def get_field_info():
    """Combine label + description per field, in feature_order — for the intro modal."""
    return [
        {
            "field": f,
            "label": pretty_label(f),
            "description": FIELD_DESCRIPTIONS.get(f, ""),
        }
        for f in feature_order
    ]


def log_prediction(payload: dict, predicted_career: str, confidence: float):
    """Append one row per prediction to data/prediction_log.csv. Best-effort —
    a logging failure should never break the actual prediction response."""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        is_new_file = not os.path.exists(LOG_PATH)

        with open(LOG_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            if is_new_file:
                writer.writerow(
                    ["timestamp"] + feature_order + ["predicted_career", "confidence"]
                )
            row = [datetime.now(timezone.utc).isoformat()]
            row += [payload[f] for f in feature_order]
            row += [predicted_career, confidence]
            writer.writerow(row)
    except Exception:
        traceback.print_exc()


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/<path:filename>")
def public_files(filename):
    # Only used for local dev — Vercel serves ICRS_Project/public/** directly
    # via its CDN and never reaches this route in production.
    file_path = os.path.join(PUBLIC_DIR, filename)
    if os.path.isfile(file_path):
        return send_from_directory(PUBLIC_DIR, filename)
    return jsonify({"error": "Not found"}), 404


@app.route("/")
def index():
    return render_template(
        "index.html",
        features=feature_order,
        ranges=get_field_ranges(),
        labels=get_field_labels(),
        field_info=get_field_info(),
        model_accuracy=model_meta.get("accuracy"),
        ready=model_ready(),
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok" if model_ready() else "model_not_loaded",
            "accuracy": model_meta.get("accuracy"),
            "num_classes": len(label_encoder.classes_) if label_encoder else 0,
            "features_expected": feature_order,
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    if not model_ready():
        return jsonify(
            {"error": "Model artifacts not loaded. Check the server logs / models/ folder."}
        ), 503

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        features = validate_and_extract(payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        scaled = scaler.transform(features)
        probabilities = model.predict_proba(scaled)[0]

        # Top prediction
        top_idx = int(np.argmax(probabilities))
        top_label = label_encoder.inverse_transform([top_idx])[0]

        # Top-3 recommendations, ranked
        ranked_idx = np.argsort(probabilities)[::-1][:3]
        top_3 = [
            {
                "career": label_encoder.inverse_transform([i])[0],
                "confidence": round(float(probabilities[i]) * 100, 2),
            }
            for i in ranked_idx
        ]

        top_confidence = round(float(probabilities[top_idx]) * 100, 2)
        low_confidence = top_confidence < CONFIDENCE_THRESHOLD

        log_prediction(payload, top_label, top_confidence)

        response = {
            "predicted_career": top_label,
            "confidence": top_confidence,
            "top_3_recommendations": top_3,
            "low_confidence": low_confidence,
        }
        if low_confidence:
            response["message"] = (
                f"No single career stood out strongly (top match only {top_confidence}%). "
                "Consider the top 3 alternatives rather than treating this as a firm result."
            )

        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # debug=True is fine for local dev/demo; turn off for your final defended build
    app.run(debug=True, host="0.0.0.0", port=5000)
