"""
RESTful JSON API endpoints for security module.
"""
from flask import Blueprint, jsonify, request, session
from modules.security.service import SecurityDomainService
from config import Config

security_api_bp = Blueprint("security_api", __name__, url_prefix="/api/v1/security")

@security_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "security", "status": "OPERATIONAL", "version": "1.0.0"})

@security_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = SecurityDomainService(Config.SECURITY_DATA_DIR if hasattr(Config, "SECURITY_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "security", "records": service.list_all()})
