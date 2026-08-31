from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.deployment_service import DeploymentService
from repositories.deployment_repo import DeploymentRepository

deployments_bp = Blueprint("deployments", __name__, url_prefix="/deployments")

def get_deployment_service() -> DeploymentService:
    repo = DeploymentRepository(current_app.config["DEPLOYMENTS_DATA_DIR"])
    return DeploymentService(repo)

@deployments_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_deployment_service()
    deployments = service.repo.get_all_deployments()
    return render_template("deployments/list.html", deployments=deployments)

@deployments_bp.route("/deploy", methods=["GET", "POST"])
def deploy():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        project_id = request.form.get("project_id", "proj_default").strip()
        environment = request.form.get("environment", "Development").strip()
        version = request.form.get("version", "v1.0.0").strip()
        require_approval = request.form.get("require_approval") == "true"
        deployed_by = session.get("username", "admin")

        service = get_deployment_service()
        success, dep, msg = service.trigger_deployment(
            project_id=project_id,
            environment=environment,
            version=version,
            deployed_by=deployed_by,
            require_approval=require_approval
        )

        flash(msg, "success" if success else "danger")
        if dep:
            return redirect(url_for("deployments.detail", deployment_id=dep.id))
        return redirect(url_for("deployments.index"))

    return render_template("deployments/deploy.html")

@deployments_bp.route("/<deployment_id>")
def detail(deployment_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_deployment_service()
    dep = service.repo.get_deployment_by_id(deployment_id)
    if not dep:
        flash("Deployment not found.", "warning")
        return redirect(url_for("deployments.index"))

    return render_template("deployments/detail.html", deployment=dep)

@deployments_bp.route("/<deployment_id>/approve", methods=["POST"])
def approve(deployment_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    approver = session.get("username", "admin")
    service = get_deployment_service()
    success, msg = service.approve_deployment(deployment_id, approver)

    flash(msg, "success" if success else "danger")
    return redirect(url_for("deployments.detail", deployment_id=deployment_id))

@deployments_bp.route("/<deployment_id>/rollback", methods=["POST"])
def rollback(deployment_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    operator = session.get("username", "admin")
    service = get_deployment_service()
    success, rollback_dep, msg = service.rollback_deployment(deployment_id, operator)

    flash(msg, "info" if success else "danger")
    if rollback_dep:
        return redirect(url_for("deployments.detail", deployment_id=rollback_dep.id))
    return redirect(url_for("deployments.detail", deployment_id=deployment_id))
