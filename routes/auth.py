from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.auth_service import AuthService
from repositories.user_repo import UserRepository

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_auth_service() -> AuthService:
    repo = UserRepository(current_app.config["USERS_DATA_DIR"])
    return AuthService(repo)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        service = get_auth_service()
        success, user, message = service.authenticate(username, password)
        
        if success and user:
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            session["full_name"] = user.full_name
            flash(message, "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))
        else:
            flash(message, "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        full_name = request.form.get("full_name", "").strip()
        role = request.form.get("role", "Developer").strip()

        service = get_auth_service()
        success, user, message = service.register_user(
            username=username,
            email=email,
            password=password,
            role=role,
            full_name=full_name
        )

        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "danger")

    return render_template("auth/register.html")

@auth_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    service = get_auth_service()
    user = service.get_user_by_id(session["user_id"])
    return render_template("auth/profile.html", user=user)

@auth_bp.route("/switch-role", methods=["POST"])
def switch_role():
    """Demo feature to allow quick role switching in local environment."""
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    new_role = request.form.get("role", "Developer")
    session["role"] = new_role
    flash(f"Switched role to {new_role} for testing.", "info")
    return redirect(request.referrer or url_for("dashboard.index"))
