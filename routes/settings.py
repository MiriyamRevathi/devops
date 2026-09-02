from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required
from services.audit_service import AuditService
from storage.json_store import JSONStore
from utils.helpers import get_utc_now_iso

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

def get_settings_store() -> JSONStore:
    return JSONStore(current_app.config["SETTINGS_DATA_DIR"], "platform_settings.json")

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

def seed_default_settings(store: JSONStore):
    if store.count() == 0:
        default_cfg = {
            "id": "global_config",
            "platform_name": "DevOpsFlow Enterprise",
            "environment_mode": "Production-Ready",
            "require_pr_review": True,
            "require_qa_signoff": True,
            "auto_rollback_on_failure": True,
            "max_concurrent_pipelines": 8,
            "session_timeout_hours": 24,
            "updated_by": "admin",
            "updated_at": get_utc_now_iso()
        }
        store.insert(default_cfg)

@settings_bp.route("/", methods=["GET"])
@login_required
@permission_required("settings.manage")
def index():
    store = get_settings_store()
    seed_default_settings(store)
    settings_data = store.find_by_id("global_config") or {}
    return render_template("settings/index.html", settings=settings_data)

@settings_bp.route("/update", methods=["POST"])
@login_required
@permission_required("settings.manage")
def update_settings():
    store = get_settings_store()
    settings_data = store.find_by_id("global_config") or {"id": "global_config"}

    settings_data["platform_name"] = request.form.get("platform_name", "DevOpsFlow Enterprise")
    settings_data["require_pr_review"] = request.form.get("require_pr_review") == "true"
    settings_data["require_qa_signoff"] = request.form.get("require_qa_signoff") == "true"
    settings_data["auto_rollback_on_failure"] = request.form.get("auto_rollback_on_failure") == "true"
    settings_data["max_concurrent_pipelines"] = int(request.form.get("max_concurrent_pipelines", 8))
    settings_data["session_timeout_hours"] = int(request.form.get("session_timeout_hours", 24))
    settings_data["updated_by"] = session.get("username", "Admin")
    settings_data["updated_at"] = get_utc_now_iso()

    store.update("global_config", settings_data)

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "Admin"),
        event_type="SETTINGS_UPDATED",
        resource="GlobalSettings",
        details="Updated platform configuration parameters."
    )

    flash("Global platform settings updated successfully.", "success")
    return redirect(url_for("settings.index"))
