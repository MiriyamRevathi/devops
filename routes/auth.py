from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import SecurityManager, login_required
from repositories.user_repo import UserRepository
from services.audit_service import AuditService
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_user_repo() -> UserRepository:
    return UserRepository(current_app.config["USERS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = SecurityManager.sanitize_input(request.form.get("username", ""))
        password = request.form.get("password", "")

        repo = get_user_repo()
        user = repo.get_by_username(username)
        audit = get_audit_service()

        if user and SecurityManager.verify_password(password, user.password_hash):
            if not user.is_active:
                flash("Your account has been deactivated. Please contact an administrator.", "danger")
                audit.record_event(
                    actor=username,
                    event_type="LOGIN_FAILED",
                    resource="AuthSystem",
                    details=f"Deactivated account '{username}' attempted login."
                )
                return render_template("auth/login.html")

            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            session["full_name"] = user.full_name

            audit.record_event(
                actor=user.username,
                event_type="LOGIN_SUCCESS",
                resource="AuthSystem",
                details=f"User '{user.username}' signed in with role '{user.role}'."
            )

            flash(f"Welcome back, {user.full_name} ({user.role})!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))
        else:
            audit.record_event(
                actor=username or "Unknown",
                event_type="LOGIN_FAILED",
                resource="AuthSystem",
                details=f"Failed login attempt for username '{username}'."
            )
            flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = SecurityManager.sanitize_input(request.form.get("username", ""))
        email = SecurityManager.sanitize_input(request.form.get("email", ""))
        password = request.form.get("password", "")
        full_name = SecurityManager.sanitize_input(request.form.get("full_name", "")) or username.capitalize()

        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("auth/register.html")

        repo = get_user_repo()
        if repo.get_by_username(username):
            flash(f"Username '{username}' is already taken.", "danger")
            return render_template("auth/register.html")

        if repo.get_by_email(email):
            flash(f"Email '{email}' is already registered.", "danger")
            return render_template("auth/register.html")

        new_user = User(
            username=username,
            email=email,
            password_hash=SecurityManager.hash_password(password),
            role="Developer",
            full_name=full_name
        )
        repo.create(new_user)

        audit = get_audit_service()
        audit.record_event(
            actor=username,
            event_type="USER_REGISTERED",
            resource=f"User:{username}",
            details=f"User '{username}' registered with role 'Developer'."
        )

        flash("Registration successful! Please sign in with your credentials.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    username = session.get("username", "Unknown")
    if "user_id" in session:
        audit = get_audit_service()
        audit.record_event(
            actor=username,
            event_type="LOGOUT",
            resource="AuthSystem",
            details=f"User '{username}' logged out."
        )

    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    repo = get_user_repo()
    user = repo.get_by_id(session.get("user_id"))
    permissions = SecurityManager.get_user_permissions(session.get("role", "Viewer"))
    return render_template("auth/profile.html", user=user, permissions=permissions)
