from flask import Blueprint, render_template, session, redirect, url_for, current_app
from repositories.project_repo import ProjectRepository
from repositories.pipeline_repo import PipelineRepository
from repositories.deployment_repo import DeploymentRepository
from repositories.service_repo import ServiceRepository
from repositories.incident_repo import IncidentRepository
from repositories.monitoring_repo import MonitoringRepository
from services.monitoring_service import MonitoringService

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    proj_repo = ProjectRepository(current_app.config["PROJECTS_DATA_DIR"])
    pipe_repo = PipelineRepository(current_app.config["PIPELINES_DATA_DIR"])
    dep_repo = DeploymentRepository(current_app.config["DEPLOYMENTS_DATA_DIR"])
    svc_repo = ServiceRepository(current_app.config["SERVICES_DATA_DIR"])
    inc_repo = IncidentRepository(current_app.config["INCIDENTS_DATA_DIR"])
    mon_repo = MonitoringRepository(current_app.config["MONITORING_DATA_DIR"])

    projects = proj_repo.get_all()
    pipelines = pipe_repo.get_all()
    pipeline_runs = pipe_repo.get_all_runs()
    deployments = dep_repo.get_all_deployments()
    services = svc_repo.get_all()
    incidents = inc_repo.get_all()

    # Calculate Summary Stats
    active_projects_count = len([p for p in projects if p.is_active()])
    successful_runs = [r for r in pipeline_runs if r.status == "SUCCESS"]
    failed_runs = [r for r in pipeline_runs if r.status == "FAILED"]
    build_success_rate = round((len(successful_runs) / len(pipeline_runs) * 100), 1) if pipeline_runs else 100.0

    prod_deployments = [d for d in deployments if d.environment == "Production" and d.status == "SUCCESS"]
    active_incidents = [i for i in incidents if i.status in ["OPEN", "INVESTIGATING", "MITIGATING"]]

    mon_service = MonitoringService(mon_repo)
    dora_metrics = mon_service.calculate_dora_metrics()

    return render_template(
        "dashboard/index.html",
        active_projects_count=active_projects_count,
        total_pipelines_count=len(pipelines),
        total_runs_count=len(pipeline_runs),
        successful_runs_count=len(successful_runs),
        failed_runs_count=len(failed_runs),
        build_success_rate=build_success_rate,
        total_deployments_count=len(deployments),
        prod_deployments_count=len(prod_deployments),
        services=services,
        active_incidents=active_incidents,
        dora=dora_metrics,
        recent_runs=pipeline_runs[:5],
        recent_deployments=deployments[:5]
    )
