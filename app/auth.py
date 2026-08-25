"""
Authentication for the ICRS.

Registered as a Flask Blueprint so it stays out of app.py's way. Every route
here checks db_enabled() first and returns a clear 503 if no database is
configured — this only ever activates on Vercel once Supabase is connected.
"""

from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from db import db, db_enabled, get_database_url, User

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()


def init_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"

    @login_manager.user_loader
    def load_user(user_id):
        if not db_enabled():
            return None
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)


def _no_database_response():
    return jsonify({
        "error": "Accounts aren't available in this environment. "
                 "This feature only works on the deployed version with a database connected."
    }), 503


@auth_bp.route("/signup", methods=["GET"])
def signup_page():
    if not db_enabled():
        return render_template("auth_unavailable.html"), 503
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET"])
def login_page():
    if not db_enabled():
        return render_template("auth_unavailable.html"), 503
    return render_template("login.html")


@auth_bp.route("/api/signup", methods=["POST"])
def api_signup():
    if not db_enabled():
        return _no_database_response()

    data = request.get_json(silent=True) or {}
    full_name = (data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not full_name or not email or not password:
        return jsonify({"error": "full_name, email, and password are all required."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with that email already exists."}), 409

    user = User(full_name=full_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({"message": "Account created.", "full_name": user.full_name}), 201


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    if not db_enabled():
        return _no_database_response()

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Incorrect email or password."}), 401

    login_user(user)
    return jsonify({"message": "Logged in.", "full_name": user.full_name}), 200


@auth_bp.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out."}), 200


@auth_bp.route("/api/me", methods=["GET"])
def api_me():
    if not db_enabled():
        return jsonify({"authenticated": False, "db_enabled": False})
    if current_user.is_authenticated:
        return jsonify({"authenticated": True, "full_name": current_user.full_name, "email": current_user.email})
    return jsonify({"authenticated": False, "db_enabled": True})
