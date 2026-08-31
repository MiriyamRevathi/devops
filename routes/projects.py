from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.project_service import ProjectService
from repositories.project_repo import ProjectRepository

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

def get_project_service() -> ProjectService:
    repo = ProjectRepository(current_app.config["PROJECTS_DATA_DIR"])
    return ProjectService(repo)

@projects_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    team = request.args.get("team", "").strip()

    service = get_project_service()
    project_list = service.list_projects(query=query, status=status, team=team)

    return render_template(
        "projects/list.html",
        projects=project_list,
        query=query,
        status=status,
        team=team
    )

@projects_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        team = request.form.get("team", "Core DevOps").strip()
        repository = request.form.get("repository", "").strip()
        default_branch = request.form.get("default_branch", "main").strip()
        environment = request.form.get("environment", "Production").strip()
        owner = session.get("username", "admin")

        service = get_project_service()
        success, project, message = service.create_project(
            name=name,
            description=description,
            owner=owner,
            team=team,
            repository=repository,
            default_branch=default_branch,
            environment=environment
        )

        if success and project:
            flash(message, "success")
            return redirect(url_for("projects.detail", project_id=project.id))
        else:
            flash(message, "danger")

    return render_template("projects/create.html")

@projects_bp.route("/<project_id>")
def detail(project_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_project_service()
    project = service.get_project(project_id)
    if not project:
        flash("Project not found.", "warning")
        return redirect(url_for("projects.index"))

    return render_template("projects/detail.html", project=project)

@projects_bp.route("/<project_id>/edit", methods=["GET", "POST"])
def edit(project_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_project_service()
    project = service.get_project(project_id)
    if not project:
        flash("Project not found.", "warning")
        return redirect(url_for("projects.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        team = request.form.get("team", project.team).strip()
        environment = request.form.get("environment", project.environment).strip()
        default_branch = request.form.get("default_branch", project.default_branch).strip()

        success, updated, message = service.update_project(
            project_id=project.id,
            name=name,
            description=description,
            team=team,
            environment=environment,
            default_branch=default_branch
        )

        if success:
            flash(message, "success")
            return redirect(url_for("projects.detail", project_id=project.id))
        else:
            flash(message, "danger")

    return render_template("projects/edit.html", project=project)

@projects_bp.route("/<project_id>/archive", methods=["POST"])
def archive(project_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_project_service()
    success, message = service.archive_project(project_id)
    flash(message, "info" if success else "danger")
    return redirect(url_for("projects.detail", project_id=project_id))

@projects_bp.route("/<project_id>/delete", methods=["POST"])
def delete(project_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_project_service()
    success, message = service.delete_project(project_id)
    flash(message, "success" if success else "danger")
    return redirect(url_for("projects.index"))
