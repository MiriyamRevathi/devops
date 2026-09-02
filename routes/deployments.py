from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from core.security import login_required, permission_required, SecurityManager
from services.deployment_service import DeploymentService
from repositories.deployment_repo import DeploymentRepository
from services.audit_service import AuditService

deployments_bp = Blueprint("deployments", __name__, url_prefix="/deployments")

def get_deploy_service() -> DeploymentService:
    repo = DeploymentRepository(current_app.config["DEPLOYMENTS_DATA_DIR"])
    return DeploymentService(repo)

def get_deploy_repo() -> DeploymentRepository:
    return DeploymentRepository(current_app.config["DEPLOYMENTS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@deployments_bp.route("/", methods=["GET"])
@login_required
@permission_required("deployment.view")
def list_deployments():
    repo = get_deploy_repo()
    deployments = repo.get_all_deployments()
    return render_template("deployments/list.html", deployments=deployments)

@deployments_bp.route("/index", methods=["GET"])
@login_required
@permission_required("deployment.view")
def index():
    return list_deployments()

@deployments_bp.route("/<deployment_id>", methods=["GET"])
@login_required
@permission_required("deployment.view")
def detail(deployment_id: str):
    repo = get_deploy_repo()
    dep = repo.get_deployment_by_id(deployment_id)
    if not dep:
        flash("Deployment record not found.", "danger")
        return redirect(url_for("deployments.list_deployments"))
    return render_template("deployments/detail.html", deployment=dep)

@deployments_bp.route("/deploy", methods=["GET", "POST"])
@login_required
@permission_required("deployment.create")
def create_deployment():
    if request.method == "POST":
        project_id = request.form.get("project_id", "PROJ-101")
        environment = request.form.get("environment", "Development")
        version = SecurityManager.sanitize_input(request.form.get("version", "1.0.0"))
        deployed_by = session.get("username", "admin")
        user_role = session.get("role", "Viewer")

        # Backend Authorization Check: Production Deployment Restriction
        if environment.lower() == "production" and user_role not in ["Admin", "DevOps Engineer"]:
            if request.is_json:
                return jsonify({
                    "error": "Forbidden",
                    "message": "Access Denied: Production deployments are strictly restricted to Admin and DevOps Engineer roles."
                }), 403
            return render_template("errors/403.html", required_role="Admin, DevOps Engineer", user_role=user_role), 403

        service = get_deploy_service()
        success, dep, msg = service.trigger_deployment(
            project_id=project_id,
            environment=environment,
            version=version,
            deployed_by=deployed_by
        )

        if success and dep:
            audit = get_audit_service()
            audit.record_event(
                actor=deployed_by,
                event_type="PRODUCTION_DEPLOYMENT" if environment.lower() == "production" else "DEPLOYMENT_TRIGGERED",
                resource=f"Deployment:{dep.id}",
                details=f"Deployed version '{version}' to environment '{environment}' with status '{dep.status}'."
            )
            flash(f"Deployment to '{environment}' triggered (Status: {dep.status}).", "success")
            return redirect(url_for("deployments.list_deployments"))
        else:
            flash(msg, "danger")

    return render_template("deployments/deploy.html")

@deployments_bp.route("/<deployment_id>/rollback", methods=["POST"])
@login_required
@permission_required("deployment.rollback")
def rollback_deployment(deployment_id: str):
    user_role = session.get("role", "Viewer")
    repo = get_deploy_repo()
    dep = repo.get_deployment_by_id(deployment_id)

    if not dep:
        flash("Deployment record not found.", "danger")
        return redirect(url_for("deployments.list_deployments"))

    # Backend Authorization Check: Production Rollback Restriction
    if dep.environment.lower() == "production" and user_role not in ["Admin", "DevOps Engineer"]:
        if request.is_json:
            return jsonify({
                "error": "Forbidden",
                "message": "Access Denied: Production rollbacks are strictly restricted to Admin and DevOps Engineer roles."
            }), 403
        return render_template("errors/403.html", required_role="Admin, DevOps Engineer", user_role=user_role), 403

    operator = session.get("username", "operator")
    service = get_deploy_service()
    success, rolled_back_dep, msg = service.rollback_deployment(deployment_id=deployment_id, operator=operator)

    if success and rolled_back_dep:
        audit = get_audit_service()
        audit.record_event(
            actor=operator,
            event_type="PRODUCTION_ROLLBACK" if dep.environment.lower() == "production" else "DEPLOYMENT_ROLLBACK",
            resource=f"Deployment:{deployment_id}",
            details=f"Rolled back environment '{dep.environment}' to version '{rolled_back_dep.version}'."
        )
        flash(f"Deployment #{deployment_id[:6]} on '{dep.environment}' rolled back successfully.", "info")
    else:
        flash(msg, "danger")

    return redirect(url_for("deployments.list_deployments"))
