from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.monitoring_service import MonitoringService
from repositories.monitoring_repo import MonitoringRepository

monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")

def get_monitoring_service() -> MonitoringService:
    repo = MonitoringRepository(current_app.config["MONITORING_DATA_DIR"])
    return MonitoringService(repo)

@monitoring_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_monitoring_service()
    service.collect_current_sample()
    samples = service.repo.get_all_samples()
    stats = service.get_aggregated_stats()

    return render_template("monitoring/dashboard.html", samples=samples, stats=stats)

@monitoring_bp.route("/api/sample", methods=["POST"])
def trigger_sample():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    service = get_monitoring_service()
    sample = service.collect_current_sample()
    return jsonify(sample.to_dict())
