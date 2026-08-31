"""
RESTful JSON API endpoints for pipelines module.
"""
from flask import Blueprint, jsonify, request, session
from modules.pipelines.service import PipelinesDomainService
from config import Config

pipelines_api_bp = Blueprint("pipelines_api", __name__, url_prefix="/api/v1/pipelines")

@pipelines_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "pipelines", "status": "OPERATIONAL", "version": "1.0.0"})

@pipelines_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = PipelinesDomainService(Config.PIPELINES_DATA_DIR if hasattr(Config, "PIPELINES_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "pipelines", "records": service.list_all()})
