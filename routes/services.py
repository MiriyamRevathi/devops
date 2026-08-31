from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.service_catalog_service import ServiceCatalogService
from repositories.service_repo import ServiceRepository

services_bp = Blueprint("services", __name__, url_prefix="/services")

def get_svc_catalog_service() -> ServiceCatalogService:
    repo = ServiceRepository(current_app.config["SERVICES_DATA_DIR"])
    return ServiceCatalogService(repo)

@services_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_svc_catalog_service()
    services = service.repo.get_all()
    return render_template("services/list.html", services=services)

@services_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        team = request.form.get("team", "Backend Platform").strip()
        version = request.form.get("version", "v1.0.0").strip()
        environment = request.form.get("environment", "Production").strip()
        owner = session.get("username", "admin")

        service = get_svc_catalog_service()
        success, svc, msg = service.create_service(
            name=name,
            owner=owner,
            team=team,
            version=version,
            environment=environment
        )

        if success and svc:
            flash(msg, "success")
            return redirect(url_for("services.detail", service_id=svc.id))
        else:
            flash(msg, "danger")

    return render_template("services/create.html")

@services_bp.route("/<service_id>")
def detail(service_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_svc_catalog_service()
    svc = service.repo.get_by_id(service_id)
    if not svc:
        flash("Service not found.", "warning")
        return redirect(url_for("services.index"))

    return render_template("services/detail.html", service=svc)

@services_bp.route("/<service_id>/restart", methods=["POST"])
def restart(service_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_svc_catalog_service()
    success, msg = service.restart_service(service_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("services.detail", service_id=service_id))
