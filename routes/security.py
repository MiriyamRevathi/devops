from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.security_scanner import SecurityScannerService

security_bp = Blueprint("security", __name__, url_prefix="/security")

def get_security_service() -> SecurityScannerService:
    return SecurityScannerService(current_app.config["SECURITY_DATA_DIR"])

@security_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_security_service()
    findings = service.run_scan()
    return render_template("security/dashboard.html", findings=findings)

@security_bp.route("/scan", methods=["POST"])
def scan():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_security_service()
    findings = service.run_scan()
    flash(f"Security scan completed. Found {len(findings)} findings.", "info")
    return redirect(url_for("security.index"))

@security_bp.route("/findings/<finding_id>/resolve", methods=["POST"])
def resolve(finding_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_security_service()
    success = service.resolve_finding(finding_id)
    flash("Finding marked as RESOLVED.", "success" if success else "danger")
    return redirect(url_for("security.index"))
