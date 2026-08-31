"""
RESTful JSON API endpoints for releases module.
"""
from flask import Blueprint, jsonify, request, session
from modules.releases.service import ReleasesDomainService
from config import Config

releases_api_bp = Blueprint("releases_api", __name__, url_prefix="/api/v1/releases")

@releases_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "releases", "status": "OPERATIONAL", "version": "1.0.0"})

@releases_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ReleasesDomainService(Config.RELEASES_DATA_DIR if hasattr(Config, "RELEASES_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "releases", "records": service.list_all()})
