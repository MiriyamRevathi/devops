"""
RESTful JSON API endpoints for audit module.
"""
from flask import Blueprint, jsonify, request, session
from modules.audit.service import AuditDomainService
from config import Config

audit_api_bp = Blueprint("audit_api", __name__, url_prefix="/api/v1/audit")

@audit_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "audit", "status": "OPERATIONAL", "version": "1.0.0"})

@audit_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = AuditDomainService(Config.AUDIT_DATA_DIR if hasattr(Config, "AUDIT_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "audit", "records": service.list_all()})
