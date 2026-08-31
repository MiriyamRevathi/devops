"""
RESTful JSON API endpoints for containers module.
"""
from flask import Blueprint, jsonify, request, session
from modules.containers.service import ContainersDomainService
from config import Config

containers_api_bp = Blueprint("containers_api", __name__, url_prefix="/api/v1/containers")

@containers_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "containers", "status": "OPERATIONAL", "version": "1.0.0"})

@containers_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ContainersDomainService(Config.CONTAINERS_DATA_DIR if hasattr(Config, "CONTAINERS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "containers", "records": service.list_all()})
