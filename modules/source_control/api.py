"""
RESTful JSON API endpoints for source_control module.
"""
from flask import Blueprint, jsonify, request, session
from modules.source_control.service import SourceControlDomainService
from config import Config

source_control_api_bp = Blueprint("source_control_api", __name__, url_prefix="/api/v1/source_control")

@source_control_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "source_control", "status": "OPERATIONAL", "version": "1.0.0"})

@source_control_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = SourceControlDomainService(Config.SOURCE_CONTROL_DATA_DIR if hasattr(Config, "SOURCE_CONTROL_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "source_control", "records": service.list_all()})
