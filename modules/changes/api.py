"""
RESTful JSON API endpoints for changes module.
"""
from flask import Blueprint, jsonify, request, session
from modules.changes.service import ChangesDomainService
from config import Config

changes_api_bp = Blueprint("changes_api", __name__, url_prefix="/api/v1/changes")

@changes_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "changes", "status": "OPERATIONAL", "version": "1.0.0"})

@changes_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = ChangesDomainService(Config.CHANGES_DATA_DIR if hasattr(Config, "CHANGES_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "changes", "records": service.list_all()})
