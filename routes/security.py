from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required
from services.security_scanner import SecurityScannerService
from services.audit_service import AuditService

security_bp = Blueprint("security", __name__, url_prefix="/security")

def get_security_service() -> SecurityScannerService:
    return SecurityScannerService(current_app.config["SECURITY_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@security_bp.route("/", methods=["GET"])
@login_required
@permission_required("security.view")
def index():
    service = get_security_service()
    findings = service.run_scan()
    return render_template("security/dashboard.html", findings=findings)

@security_bp.route("/scan", methods=["POST"])
@login_required
@permission_required("security.scan")
def trigger_scan():
    service = get_security_service()
    findings = service.run_scan()

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "Unknown"),
        event_type="SECURITY_SCAN_EXECUTED",
        resource="SecurityScanner",
        details=f"Executed security scan. Discovered {len(findings)} findings."
    )

    flash(f"Security scan executed. Discovered {len(findings)} security findings.", "info")
    return redirect(url_for("security.index"))

@security_bp.route("/findings/<finding_id>/resolve", methods=["POST"])
@login_required
@permission_required("security.scan")
def resolve_finding(finding_id: str):
    service = get_security_service()
    if service.resolve_finding(finding_id):
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="SECURITY_FINDING_RESOLVED",
            resource=f"Finding:{finding_id}",
            details=f"Resolved security finding #{finding_id}."
        )
        flash(f"Security finding #{finding_id} marked as RESOLVED.", "success")
    return redirect(url_for("security.index"))
