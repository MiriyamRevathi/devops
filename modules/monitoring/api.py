"""
RESTful JSON API endpoints for monitoring module.
"""
from flask import Blueprint, jsonify, request, session
from modules.monitoring.service import MonitoringDomainService
from config import Config

monitoring_api_bp = Blueprint("monitoring_api", __name__, url_prefix="/api/v1/monitoring")

@monitoring_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "monitoring", "status": "OPERATIONAL", "version": "1.0.0"})

@monitoring_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = MonitoringDomainService(Config.MONITORING_DATA_DIR if hasattr(Config, "MONITORING_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "monitoring", "records": service.list_all()})
