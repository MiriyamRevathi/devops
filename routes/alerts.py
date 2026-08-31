from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.alert_service import AlertService
from repositories.alert_repo import AlertRepository

alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")

def get_alert_service() -> AlertService:
    repo = AlertRepository(current_app.config["ALERTS_DATA_DIR"])
    return AlertService(repo)

@alerts_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_alert_service()
    rules = service.repo.get_all()
    return render_template("alerts/list.html", rules=rules)

@alerts_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        metric = request.form.get("metric", "CPU").strip()
        condition = request.form.get("condition", ">").strip()
        threshold = float(request.form.get("threshold", 80.0))
        svc_name = request.form.get("service", "All").strip()

        service = get_alert_service()
        success, rule, msg = service.create_rule(
            name=name,
            metric=metric,
            condition=condition,
            threshold=threshold,
            service=svc_name
        )

        if success:
            flash(msg, "success")
            return redirect(url_for("alerts.index"))
        else:
            flash(msg, "danger")

    return render_template("alerts/create.html")

@alerts_bp.route("/<alert_id>/trigger", methods=["POST"])
def trigger(alert_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_alert_service()
    success, msg = service.trigger_simulation(alert_id)
    flash(msg, "warning" if success else "danger")
    return redirect(url_for("alerts.index"))

@alerts_bp.route("/<alert_id>/resolve", methods=["POST"])
def resolve(alert_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_alert_service()
    success, msg = service.resolve_alert(alert_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("alerts.index"))
