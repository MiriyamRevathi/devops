"""
RESTful JSON API endpoints for environments module.
"""
from flask import Blueprint, jsonify, request, session
from modules.environments.service import EnvironmentsDomainService
from config import Config

environments_api_bp = Blueprint("environments_api", __name__, url_prefix="/api/v1/environments")

@environments_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "environments", "status": "OPERATIONAL", "version": "1.0.0"})

@environments_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = EnvironmentsDomainService(Config.ENVIRONMENTS_DATA_DIR if hasattr(Config, "ENVIRONMENTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "environments", "records": service.list_all()})
