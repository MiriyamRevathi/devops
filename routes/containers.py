from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.container_engine import ContainerEngine
from repositories.container_repo import ContainerRepository
from services.audit_service import AuditService
from models.container import Container

containers_bp = Blueprint("containers", __name__, url_prefix="/containers")

def get_container_engine() -> ContainerEngine:
    repo = ContainerRepository(current_app.config["CONTAINERS_DATA_DIR"])
    return ContainerEngine(repo)

def get_container_repo() -> ContainerRepository:
    return ContainerRepository(current_app.config["CONTAINERS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@containers_bp.route("/", methods=["GET"])
@login_required
@permission_required("container.view")
def list_containers():
    repo = get_container_repo()
    containers = repo.get_all()
    return render_template("containers/list.html", containers=containers)

@containers_bp.route("/create", methods=["POST"])
@login_required
@permission_required("container.create")
def create_container():
    name = SecurityManager.sanitize_input(request.form.get("name", "devopsflow-microservice"))
    image = SecurityManager.sanitize_input(request.form.get("image", "nginx:alpine"))

    repo = get_container_repo()
    cnt = Container(name=name, image=image, ports="8080:80")
    repo.save(cnt)

    audit = get_audit_service()
    audit.record_event(
        actor=session.get("username", "Unknown"),
        event_type="CONTAINER_CREATED",
        resource=f"Container:{name}",
        details=f"Created container '{name}' with image '{image}'."
    )

    flash(f"Container '{name}' created.", "success")
    return redirect(url_for("containers.list_containers"))

@containers_bp.route("/<container_id>/start", methods=["POST"])
@login_required
@permission_required("container.start")
def start_container(container_id: str):
    engine = get_container_engine()
    success, msg = engine.start_container(container_id)
    if success:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="CONTAINER_STARTED",
            resource=f"Container:{container_id}",
            details=msg
        )
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for("containers.list_containers"))

@containers_bp.route("/<container_id>/stop", methods=["POST"])
@login_required
@permission_required("container.stop")
def stop_container(container_id: str):
    engine = get_container_engine()
    success, msg = engine.stop_container(container_id)
    if success:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="CONTAINER_STOPPED",
            resource=f"Container:{container_id}",
            details=msg
        )
        flash(msg, "warning")
    else:
        flash(msg, "danger")
    return redirect(url_for("containers.list_containers"))

@containers_bp.route("/<container_id>/restart", methods=["POST"])
@login_required
@permission_required("container.restart")
def restart_container(container_id: str):
    engine = get_container_engine()
    success, msg = engine.restart_container(container_id)
    if success:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="CONTAINER_RESTARTED",
            resource=f"Container:{container_id}",
            details=msg
        )
        flash(msg, "info")
    else:
        flash(msg, "danger")
    return redirect(url_for("containers.list_containers"))

@containers_bp.route("/<container_id>/remove", methods=["POST"])
@login_required
@permission_required("container.remove")
def remove_container(container_id: str):
    engine = get_container_engine()
    success, msg = engine.remove_container(container_id)
    if success:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="CONTAINER_REMOVED",
            resource=f"Container:{container_id}",
            details=msg
        )
        flash(msg, "info")
    else:
        flash(msg, "danger")
    return redirect(url_for("containers.list_containers"))
