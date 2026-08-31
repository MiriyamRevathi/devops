"""
RESTful JSON API endpoints for teams module.
"""
from flask import Blueprint, jsonify, request, session
from modules.teams.service import TeamsDomainService
from config import Config

teams_api_bp = Blueprint("teams_api", __name__, url_prefix="/api/v1/teams")

@teams_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "teams", "status": "OPERATIONAL", "version": "1.0.0"})

@teams_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = TeamsDomainService(Config.TEAMS_DATA_DIR if hasattr(Config, "TEAMS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "teams", "records": service.list_all()})
