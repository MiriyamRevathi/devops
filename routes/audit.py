from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.audit_service import AuditService
from repositories.audit_repo import AuditRepository

audit_bp = Blueprint("audit", __name__, url_prefix="/audit")

def get_audit_service() -> AuditService:
    repo = AuditRepository(current_app.config["AUDIT_DATA_DIR"])
    return AuditService(repo)

@audit_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    query = request.args.get("q", "").strip()
    event_type = request.args.get("event_type", "All").strip()
    actor = request.args.get("actor", "All").strip()

    service = get_audit_service()
    events = service.query_audit_trail(query=query, event_type=event_type, actor=actor)

    return render_template(
        "audit/list.html",
        events=events,
        query=query,
        event_type=event_type,
        actor=actor
    )
