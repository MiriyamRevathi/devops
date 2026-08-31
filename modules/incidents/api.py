"""
RESTful JSON API endpoints for incidents module.
"""
from flask import Blueprint, jsonify, request, session
from modules.incidents.service import IncidentsDomainService
from config import Config

incidents_api_bp = Blueprint("incidents_api", __name__, url_prefix="/api/v1/incidents")

@incidents_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "incidents", "status": "OPERATIONAL", "version": "1.0.0"})

@incidents_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = IncidentsDomainService(Config.INCIDENTS_DATA_DIR if hasattr(Config, "INCIDENTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "incidents", "records": service.list_all()})
