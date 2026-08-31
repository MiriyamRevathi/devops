"""
RESTful JSON API endpoints for projects module.
"""
from flask import Blueprint, jsonify, request, session
from modules.projects.service import ProjectsDomainService
from config import Config

projects_api_bp = Blueprint("projects_api", __name__, url_prefix="/api/v1/projects")

@projects_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "projects", "status": "OPERATIONAL", "version": "1.0.0"})

@projects_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ProjectsDomainService(Config.PROJECTS_DATA_DIR if hasattr(Config, "PROJECTS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "projects", "records": service.list_all()})
