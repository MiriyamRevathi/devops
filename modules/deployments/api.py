"""
RESTful JSON API endpoints for deployments module.
"""
from flask import Blueprint, jsonify, request, session
from modules.deployments.service import DeploymentsDomainService
from config import Config

deployments_api_bp = Blueprint("deployments_api", __name__, url_prefix="/api/v1/deployments")

@deployments_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "deployments", "status": "OPERATIONAL", "version": "1.0.0"})

@deployments_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = DeploymentsDomainService(Config.DEPLOYMENTS_DATA_DIR if hasattr(Config, "DEPLOYMENTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "deployments", "records": service.list_all()})
