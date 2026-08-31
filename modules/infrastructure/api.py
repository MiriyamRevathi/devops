"""
RESTful JSON API endpoints for infrastructure module.
"""
from flask import Blueprint, jsonify, request, session
from modules.infrastructure.service import InfrastructureDomainService
from config import Config

infrastructure_api_bp = Blueprint("infrastructure_api", __name__, url_prefix="/api/v1/infrastructure")

@infrastructure_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "infrastructure", "status": "OPERATIONAL", "version": "1.0.0"})

@infrastructure_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = InfrastructureDomainService(Config.INFRASTRUCTURE_DATA_DIR if hasattr(Config, "INFRASTRUCTURE_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "infrastructure", "records": service.list_all()})
