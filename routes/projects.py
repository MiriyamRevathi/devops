from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.project_service import ProjectService
from repositories.project_repo import ProjectRepository
from services.audit_service import AuditService
from models.project import Project

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

def get_project_service() -> ProjectService:
    repo = ProjectRepository(current_app.config["PROJECTS_DATA_DIR"])
    return ProjectService(repo)

def get_project_repo() -> ProjectRepository:
    return ProjectRepository(current_app.config["PROJECTS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@projects_bp.route("/", methods=["GET"])
@login_required
@permission_required("project.view")
def list_projects():
    repo = get_project_repo()
    projects = repo.get_all()
    return render_template("projects/list.html", projects=projects)

@projects_bp.route("/index", methods=["GET"])
@login_required
@permission_required("project.view")
def index():
    return list_projects()

@projects_bp.route("/<project_id>", methods=["GET"])
@login_required
@permission_required("project.view")
def detail(project_id: str):
    service = get_project_service()
    project = service.get_project(project_id)
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("projects.list_projects"))
    return render_template("projects/detail.html", project=project)

@projects_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("project.create")
def create():
    if request.method == "POST":
        name = SecurityManager.sanitize_input(request.form.get("name", ""))
        description = SecurityManager.sanitize_input(request.form.get("description", ""))
        owner = session.get("username", "admin")

        if not name:
            flash("Project Name is required.", "danger")
            return render_template("projects/create.html")

        service = get_project_service()
        success, new_proj, msg = service.create_project(name=name, description=description, owner=owner)

        if success and new_proj:
            audit = get_audit_service()
            audit.record_event(
                actor=session.get("username", "Unknown"),
                event_type="PROJECT_CREATED",
                resource=f"Project:{new_proj.id}",
                details=f"Created project '{name}'."
            )
            flash(f"Project '{name}' created successfully.", "success")
            return redirect(url_for("projects.list_projects"))
        else:
            flash(msg, "danger")

    return render_template("projects/create.html")

@projects_bp.route("/<project_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("project.edit")
def edit(project_id: str):
    service = get_project_service()
    project = service.get_project(project_id)
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("projects.list_projects"))

    if request.method == "POST":
        name = SecurityManager.sanitize_input(request.form.get("name", project.name))
        description = SecurityManager.sanitize_input(request.form.get("description", project.description))
        team = request.form.get("team", project.team)
        environment = request.form.get("environment", project.environment)
        default_branch = request.form.get("default_branch", project.default_branch)

        success, updated, msg = service.update_project(
            project_id=project_id,
            name=name,
            description=description,
            team=team,
            environment=environment,
            default_branch=default_branch
        )

        if success and updated:
            audit = get_audit_service()
            audit.record_event(
                actor=session.get("username", "Unknown"),
                event_type="PROJECT_UPDATED",
                resource=f"Project:{project.id}",
                details=f"Updated project details for '{name}'."
            )
            flash(f"Project '{name}' updated successfully.", "success")
            return redirect(url_for("projects.detail", project_id=project_id))
        else:
            flash(msg, "danger")

    return render_template("projects/edit.html", project=project)

@projects_bp.route("/<project_id>/delete", methods=["POST"])
@login_required
@permission_required("project.delete")
def delete(project_id: str):
    service = get_project_service()
    project = service.get_project(project_id)
    if project:
        name = project.name
        service.delete_project(project_id)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="PROJECT_DELETED",
            resource=f"Project:{project_id}",
            details=f"Deleted project '{name}'."
        )

        flash(f"Project '{name}' deleted.", "info")
    return redirect(url_for("projects.list_projects"))
