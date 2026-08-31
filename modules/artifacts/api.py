"""
RESTful JSON API endpoints for artifacts module.
"""
from flask import Blueprint, jsonify, request, session
from modules.artifacts.service import ArtifactsDomainService
from config import Config

artifacts_api_bp = Blueprint("artifacts_api", __name__, url_prefix="/api/v1/artifacts")

@artifacts_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "artifacts", "status": "OPERATIONAL", "version": "1.0.0"})

@artifacts_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ArtifactsDomainService(Config.ARTIFACTS_DATA_DIR if hasattr(Config, "ARTIFACTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "artifacts", "records": service.list_all()})
