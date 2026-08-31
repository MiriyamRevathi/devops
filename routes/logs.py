from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.log_service import LogService
from repositories.log_repo import LogRepository

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")

def get_log_service() -> LogService:
    repo = LogRepository(current_app.config["LOGS_DATA_DIR"])
    return LogService(repo)

@logs_bp.route("/")
def viewer():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = request.args.get("service", "All").strip()
    environment = request.args.get("environment", "All").strip()
    severity = request.args.get("severity", "All").strip()
    query = request.args.get("q", "").strip()

    log_svc = get_log_service()
    logs = log_svc.search_logs(
        service=service,
        environment=environment,
        severity=severity,
        query=query
    )

    return render_template(
        "logs/viewer.html",
        logs=logs,
        service=service,
        environment=environment,
        severity=severity,
        query=query
    )
