"""
RESTful JSON API endpoints for logs module.
"""
from flask import Blueprint, jsonify, request, session
from modules.logs.service import LogsDomainService
from config import Config

logs_api_bp = Blueprint("logs_api", __name__, url_prefix="/api/v1/logs")

@logs_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "logs", "status": "OPERATIONAL", "version": "1.0.0"})

@logs_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = LogsDomainService(Config.LOGS_DATA_DIR if hasattr(Config, "LOGS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "logs", "records": service.list_all()})
