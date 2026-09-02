from flask import Blueprint, render_template, current_app
from core.security import login_required, permission_required
from services.audit_service import AuditService

audit_bp = Blueprint("audit", __name__, url_prefix="/audit")

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@audit_bp.route("/", methods=["GET"])
@login_required
@permission_required("audit.view")
def list_logs():
    service = get_audit_service()
    logs = service.get_recent_events(100)
    return render_template("audit/list.html", logs=logs)
