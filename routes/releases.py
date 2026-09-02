from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from storage.json_store import JSONStore
from services.audit_service import AuditService
from utils.helpers import get_utc_now_iso, generate_id

releases_bp = Blueprint("releases", __name__, url_prefix="/releases")

def get_releases_store() -> JSONStore:
    return JSONStore(current_app.config["RELEASES_DATA_DIR"], "releases.json")

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

def seed_releases(store: JSONStore):
    if store.count() == 0:
        rel = {
            "id": generate_id("rel"),
            "version": "v1.4.0",
            "name": "Enterprise Governance & RBAC Release",
            "environment": "Staging",
            "status": "APPROVED",
            "qa_status": "APPROVED",
            "created_by": "admin",
            "created_at": get_utc_now_iso()
        }
        store.insert(rel)

@releases_bp.route("/", methods=["GET"])
@login_required
@permission_required("release.view")
def index():
    store = get_releases_store()
    seed_releases(store)
    releases = store.read_all()
    return render_template("releases/list.html", releases=releases)

@releases_bp.route("/<release_id>", methods=["GET"])
@login_required
@permission_required("release.view")
def detail(release_id: str):
    store = get_releases_store()
    rel = store.find_by_id(release_id)
    if not rel:
        flash("Release not found.", "danger")
        return redirect(url_for("releases.index"))
    return render_template("releases/detail.html", release=rel)

@releases_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("release.create")
def create():
    if request.method == "POST":
        version = SecurityManager.sanitize_input(request.form.get("version", "v1.5.0"))
        name = SecurityManager.sanitize_input(request.form.get("name", ""))
        environment = request.form.get("environment", "Staging")

        store = get_releases_store()
        rel = {
            "id": generate_id("rel"),
            "version": version,
            "name": name,
            "environment": environment,
            "status": "DRAFT",
            "qa_status": "PENDING",
            "created_by": session.get("username", "admin"),
            "created_at": get_utc_now_iso()
        }
        store.insert(rel)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="RELEASE_CREATED",
            resource=f"Release:{version}",
            details=f"Created release '{version}' ({name})."
        )

        flash(f"Release '{version}' created.", "success")
        return redirect(url_for("releases.index"))

    return render_template("releases/create.html")

@releases_bp.route("/<release_id>/qa-signoff", methods=["POST"])
@login_required
@permission_required("release.qa_approve")
def qa_signoff(release_id: str):
    action = request.form.get("action", "APPROVE")
    store = get_releases_store()
    rel = store.find_by_id(release_id)

    if rel:
        status_val = "APPROVED" if action == "APPROVE" else "REJECTED"
        rel["qa_status"] = status_val
        store.update(release_id, rel)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "QA Lead"),
            event_type="RELEASE_QA_SIGNOFF",
            resource=f"Release:{release_id}",
            details=f"QA Signoff for release '{rel['version']}': {status_val}."
        )

        flash(f"QA Signoff for release '{rel['version']}' set to {status_val}.", "info")
    return redirect(url_for("releases.index"))
