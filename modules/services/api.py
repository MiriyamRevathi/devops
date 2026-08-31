"""
RESTful JSON API endpoints for services module.
"""
from flask import Blueprint, jsonify, request, session
from modules.services.service import ServicesDomainService
from config import Config

services_api_bp = Blueprint("services_api", __name__, url_prefix="/api/v1/services")

@services_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "services", "status": "OPERATIONAL", "version": "1.0.0"})

@services_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ServicesDomainService(Config.SERVICES_DATA_DIR if hasattr(Config, "SERVICES_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "services", "records": service.list_all()})
