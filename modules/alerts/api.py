"""
RESTful JSON API endpoints for alerts module.
"""
from flask import Blueprint, jsonify, request, session
from modules.alerts.service import AlertsDomainService
from config import Config

alerts_api_bp = Blueprint("alerts_api", __name__, url_prefix="/api/v1/alerts")

@alerts_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "alerts", "status": "OPERATIONAL", "version": "1.0.0"})

@alerts_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = AlertsDomainService(Config.ALERTS_DATA_DIR if hasattr(Config, "ALERTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "alerts", "records": service.list_all()})
