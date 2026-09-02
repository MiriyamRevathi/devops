from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from core.security import login_required, permission_required, SecurityManager
from repositories.user_repo import UserRepository
from services.audit_service import AuditService
from models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")

def get_user_repo() -> UserRepository:
    return UserRepository(current_app.config["USERS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@users_bp.route("/", methods=["GET"])
@login_required
@permission_required("user.manage")
def list_users():
    repo = get_user_repo()
    users = repo.get_all()
    roles = list(current_app.config["ROLES"].keys())
    return render_template("users/list.html", users=users, available_roles=roles)

@users_bp.route("/create", methods=["POST"])
@login_required
@permission_required("user.manage")
def create_user():
    username = SecurityManager.sanitize_input(request.form.get("username", ""))
    email = SecurityManager.sanitize_input(request.form.get("email", ""))
    password = request.form.get("password", "")
    role = request.form.get("role", "Viewer")
    full_name = SecurityManager.sanitize_input(request.form.get("full_name", ""))

    if not username or not email or not password:
        flash("Username, email, and password are required.", "danger")
        return redirect(url_for("users.list_users"))

    repo = get_user_repo()
    if repo.get_by_username(username):
        flash(f"Username '{username}' is already taken.", "danger")
        return redirect(url_for("users.list_users"))

    new_user = User(
        username=username,
        email=email,
        password_hash=SecurityManager.hash_password(password),
        role=role,
        full_name=full_name
    )
    repo.create(new_user)

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "Admin"),
        event_type="USER_CREATED",
        resource=f"User:{username}",
        details=f"Created user '{username}' with role '{role}'."
    )

    flash(f"User '{username}' created successfully as '{role}'.", "success")
    return redirect(url_for("users.list_users"))

@users_bp.route("/<user_id>/update-role", methods=["POST"])
@login_required
@permission_required("user.manage")
def update_role(user_id: str):
    new_role = request.form.get("role")
    repo = get_user_repo()
    target_user = repo.get_by_id(user_id)

    if not target_user:
        flash("User not found.", "danger")
        return redirect(url_for("users.list_users"))

    # Admin safety rule check
    if target_user.id == session.get("user_id") and new_role != "Admin":
        flash("Safety Rule Violation: You cannot remove your own administrative privileges.", "danger")
        return redirect(url_for("users.list_users"))

    try:
        old_role = target_user.role
        target_user.role = new_role
        repo.update(target_user)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Admin"),
            event_type="ROLE_CHANGED",
            resource=f"User:{target_user.username}",
            details=f"Changed role from '{old_role}' to '{new_role}'."
        )
        flash(f"Updated role for '{target_user.username}' to '{new_role}'.", "success")
    except ValueError as ve:
        flash(str(ve), "danger")

    return redirect(url_for("users.list_users"))

@users_bp.route("/<user_id>/toggle-status", methods=["POST"])
@login_required
@permission_required("user.manage")
def toggle_status(user_id: str):
    repo = get_user_repo()
    target_user = repo.get_by_id(user_id)

    if not target_user:
        flash("User not found.", "danger")
        return redirect(url_for("users.list_users"))

    if target_user.id == session.get("user_id"):
        flash("Safety Rule Violation: You cannot deactivate your own account.", "danger")
        return redirect(url_for("users.list_users"))

    try:
        target_user.is_active = not target_user.is_active
        repo.update(target_user)

        status_str = "activated" if target_user.is_active else "deactivated"
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Admin"),
            event_type="USER_STATUS_TOGGLED",
            resource=f"User:{target_user.username}",
            details=f"User '{target_user.username}' account {status_str}."
        )
        flash(f"User '{target_user.username}' {status_str}.", "info")
    except ValueError as ve:
        flash(str(ve), "danger")

    return redirect(url_for("users.list_users"))

@users_bp.route("/<user_id>/delete", methods=["POST"])
@login_required
@permission_required("user.manage")
def delete_user(user_id: str):
    repo = get_user_repo()
    target_user = repo.get_by_id(user_id)

    if not target_user:
        flash("User not found.", "danger")
        return redirect(url_for("users.list_users"))

    if target_user.id == session.get("user_id"):
        flash("Safety Rule Violation: You cannot delete your own logged-in Admin account.", "danger")
        return redirect(url_for("users.list_users"))

    try:
        username = target_user.username
        repo.delete(user_id)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Admin"),
            event_type="USER_DELETED",
            resource=f"User:{username}",
            details=f"Deleted user '{username}'."
        )
        flash(f"User '{username}' deleted successfully.", "success")
    except ValueError as ve:
        flash(str(ve), "danger")

    return redirect(url_for("users.list_users"))
