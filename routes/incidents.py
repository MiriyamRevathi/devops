from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.incident_service import IncidentService
from repositories.incident_repo import IncidentRepository

incidents_bp = Blueprint("incidents", __name__, url_prefix="/incidents")

def get_incident_service() -> IncidentService:
    repo = IncidentRepository(current_app.config["INCIDENTS_DATA_DIR"])
    return IncidentService(repo)

@incidents_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_incident_service()
    incidents = service.repo.get_all()
    return render_template("incidents/list.html", incidents=incidents)

@incidents_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        svc_name = request.form.get("service", "API Gateway").strip()
        environment = request.form.get("environment", "Production").strip()
        severity = request.form.get("severity", "HIGH").strip()
        summary = request.form.get("summary", "").strip()
        assignee = request.form.get("assignee", session.get("username", "admin")).strip()

        service = get_incident_service()
        success, inc, msg = service.create_incident(
            title=title,
            service=svc_name,
            environment=environment,
            severity=severity,
            summary=summary,
            assignee=assignee
        )

        if success and inc:
            flash(msg, "success")
            return redirect(url_for("incidents.detail", incident_id=inc.id))
        else:
            flash(msg, "danger")

    return render_template("incidents/create.html")

@incidents_bp.route("/<incident_id>")
def detail(incident_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_incident_service()
    inc = service.repo.get_by_id(incident_id)
    if not inc:
        flash("Incident not found.", "warning")
        return redirect(url_for("incidents.index"))

    return render_template("incidents/detail.html", incident=inc)

@incidents_bp.route("/<incident_id>/status", methods=["POST"])
def update_status(incident_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    new_status = request.form.get("status", "").strip()
    notes = request.form.get("notes", "").strip()
    actor = session.get("username", "admin")

    service = get_incident_service()
    success, msg = service.update_status(incident_id, new_status, actor=actor, notes=notes)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("incidents.detail", incident_id=incident_id))

@incidents_bp.route("/<incident_id>/assign", methods=["POST"])
def assign(incident_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    assignee = request.form.get("assignee", "").strip()
    actor = session.get("username", "admin")

    service = get_incident_service()
    success, msg = service.assign_incident(incident_id, assignee, actor=actor)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("incidents.detail", incident_id=incident_id))
