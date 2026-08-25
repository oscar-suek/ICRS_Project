"""
Database layer for the ICRS.

Only active when a Postgres connection string is present in the environment
(i.e. on Vercel, once the Supabase integration injects it). Locally, without
one of these variables set, db_enabled() returns False and every route that
needs the database degrades gracefully instead of crashing — the core
prediction feature keeps working exactly as before either way.
"""

import os
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Supabase/Vercel integrations have used different names for the injected
# connection string across versions — check them in order and use whichever
# is actually present rather than assuming one.
_CANDIDATE_ENV_VARS = [
    "DATABASE_URL",
    "POSTGRES_URL",
    "POSTGRES_PRISMA_URL",
    "POSTGRES_URL_NON_POOLING",
    "SUPABASE_DB_URL",
]


def get_database_url():
    for name in _CANDIDATE_ENV_VARS:
        value = os.environ.get(name)
        if value:
            # SQLAlchemy's psycopg driver wants "postgresql://", but some
            # providers hand out "postgres://" — normalize it.
            if value.startswith("postgres://"):
                value = "postgresql://" + value[len("postgres://"):]
            return value
    return None


def db_enabled():
    return get_database_url() is not None


# ---------------------------------------------------------------------------
# Models — mirrors the ERD in Chapter 3 (USERS / ASSESSMENTS / PREDICTIONS)
# ---------------------------------------------------------------------------

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    assessments = db.relationship("Assessment", backref="user", lazy=True)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    cgpa = db.Column(db.Float, nullable=False)
    math = db.Column(db.Float, nullable=False)
    english = db.Column(db.Float, nullable=False)
    science = db.Column(db.Float, nullable=False)
    programming = db.Column(db.Float, nullable=False)
    communication = db.Column(db.Float, nullable=False)
    leadership = db.Column(db.Float, nullable=False)
    creativity = db.Column(db.Float, nullable=False)
    analytical = db.Column(db.Float, nullable=False)
    interest_tech = db.Column(db.Float, nullable=False)
    interest_business = db.Column(db.Float, nullable=False)
    interest_health = db.Column(db.Float, nullable=False)
    interest_law = db.Column(db.Float, nullable=False)
    interest_arts = db.Column(db.Float, nullable=False)
    interest_education = db.Column(db.Float, nullable=False)

    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    prediction = db.relationship("Prediction", backref="assessment", uselist=False, lazy=True)

    def to_feature_dict(self, feature_order):
        return {f: getattr(self, f) for f in feature_order}


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)

    predicted_career = db.Column(db.String(120), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    top_3_json = db.Column(db.Text, nullable=False)
    low_confidence = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


def init_db(app):
    """Call once at startup. No-op (app still runs fine) if no DB is configured."""
    url = get_database_url()
    if not url:
        return False

    app.config["SQLALCHEMY_DATABASE_URI"] = url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return True
