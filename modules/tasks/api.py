"""
RESTful JSON API endpoints for tasks module.
"""
from flask import Blueprint, jsonify, request, session
from modules.tasks.service import TasksDomainService
from config import Config

tasks_api_bp = Blueprint("tasks_api", __name__, url_prefix="/api/v1/tasks")

@tasks_api_bp.route("/status", methods=["GET"])
def get_status():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"module": "tasks", "status": "OPERATIONAL", "version": "1.0.0"})

@tasks_api_bp.route("/records", methods=["GET"])
def get_records():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    service = TasksDomainService(Config.TASKS_DATA_DIR if hasattr(Config, "TASKS_DATA_DIR") else Config.DATA_DIRECTORY)
    return jsonify({"module": "tasks", "records": service.list_all()})
