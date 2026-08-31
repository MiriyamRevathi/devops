from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.monitoring_service import MonitoringService
from repositories.monitoring_repo import MonitoringRepository

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

def get_monitoring_service() -> MonitoringService:
    repo = MonitoringRepository(current_app.config["MONITORING_DATA_DIR"])
    return MonitoringService(repo)

@analytics_bp.route("/dora")
def dora():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_monitoring_service()
    dora_results = service.calculate_dora_metrics()
    benchmarks = current_app.config.get("DORA_BENCHMARKS", {})

    return render_template("analytics/dora.html", dora=dora_results, benchmarks=benchmarks)
