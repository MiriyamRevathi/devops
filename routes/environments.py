from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.environment_service import EnvironmentService
from repositories.environment_repo import EnvironmentRepository

environments_bp = Blueprint("environments", __name__, url_prefix="/environments")

def get_env_service() -> EnvironmentService:
    repo = EnvironmentRepository(current_app.config["ENVIRONMENTS_DATA_DIR"])
    return EnvironmentService(repo)

@environments_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_env_service()
    envs = service.list_environments()
    return render_template("environments/list.html", environments=envs)

@environments_bp.route("/<env_id>")
def detail(env_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_env_service()
    env = service.get_environment(env_id)
    if not env:
        flash("Environment not found.", "warning")
        return redirect(url_for("environments.index"))

    return render_template("environments/detail.html", environment=env)

@environments_bp.route("/<env_id>/variables", methods=["POST"])
def set_variable(env_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()

    service = get_env_service()
    success, msg = service.set_environment_variable(env_id, key, value)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("environments.detail", env_id=env_id))

@environments_bp.route("/<env_id>/health-check", methods=["POST"])
def health_check(env_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_env_service()
    success, status, msg = service.trigger_health_check(env_id)
    flash(msg, "info" if success else "danger")
    return redirect(url_for("environments.detail", env_id=env_id))
