"""
RESTful JSON API endpoints for auth module.
"""
from flask import Blueprint, jsonify, request, session
from modules.auth.service import AuthDomainService
from config import Config

auth_api_bp = Blueprint("auth_api", __name__, url_prefix="/api/v1/auth")

@auth_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "auth", "status": "OPERATIONAL", "version": "1.0.0"})

@auth_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = AuthDomainService(Config.AUTH_DATA_DIR if hasattr(Config, "AUTH_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "auth", "records": service.list_all()})
