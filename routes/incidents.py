from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.incident_service import IncidentService
from services.audit_service import AuditService
from models.incident import Incident

incidents_bp = Blueprint("incidents", __name__, url_prefix="/incidents")

def get_incident_service() -> IncidentService:
    return IncidentService(current_app.config["INCIDENTS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@incidents_bp.route("/", methods=["GET"])
@login_required
@permission_required("incident.view")
def list_incidents():
    service = get_incident_service()
    incidents = service.get_all_incidents()
    return render_template("incidents/list.html", incidents=incidents)

@incidents_bp.route("/<incident_id>", methods=["GET"])
@login_required
@permission_required("incident.view")
def detail(incident_id: str):
    service = get_incident_service()
    inc = service.get_incident_by_id(incident_id)
    if not inc:
        flash("Incident record not found.", "danger")
        return redirect(url_for("incidents.list_incidents"))
    return render_template("incidents/detail.html", incident=inc)

@incidents_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("incident.create")
def create():
    if request.method == "POST":
        title = SecurityManager.sanitize_input(request.form.get("title", ""))
        severity = request.form.get("severity", "SEV-2")
        service_id = request.form.get("service_id", "SVC-API-GW")
        description = SecurityManager.sanitize_input(request.form.get("description", ""))
        reporter = session.get("username", "qa")

        if not title:
            flash("Incident Title is required.", "danger")
            return render_template("incidents/create.html")

        service = get_incident_service()
        inc = Incident(title=title, severity=severity, service_id=service_id, description=description, reporter=reporter)
        service.create_incident(inc)

        audit = get_audit_service()
        audit.record_event(
            actor=reporter,
            event_type="INCIDENT_CREATED",
            resource=f"Incident:{inc.id}",
            details=f"Reported incident '{title}' with severity '{severity}'."
        )

        flash(f"Incident '{title}' reported successfully.", "success")
        return redirect(url_for("incidents.list_incidents"))

    return render_template("incidents/create.html")

@incidents_bp.route("/<incident_id>/resolve", methods=["POST"])
@login_required
@permission_required("incident.resolve")
def resolve(incident_id: str):
    service = get_incident_service()
    resolution = SecurityManager.sanitize_input(request.form.get("resolution", "Resolved by engineer."))
    inc = service.resolve_incident(incident_id, resolution)
    if inc:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="INCIDENT_RESOLVED",
            resource=f"Incident:{incident_id}",
            details=f"Resolved incident '{inc.title}' with resolution '{resolution}'."
        )
        flash(f"Incident '{inc.title}' set to RESOLVED.", "success")
    return redirect(url_for("incidents.list_incidents"))
