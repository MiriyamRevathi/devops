from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.container_engine import ContainerEngine
from repositories.container_repo import ContainerRepository

containers_bp = Blueprint("containers", __name__, url_prefix="/containers")

def get_container_engine() -> ContainerEngine:
    repo = ContainerRepository(current_app.config["CONTAINERS_DATA_DIR"])
    return ContainerEngine(repo)

@containers_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_container_engine()
    containers = engine.repo.get_all()
    return render_template("containers/list.html", containers=containers)

@containers_bp.route("/<container_id>")
def detail(container_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_container_engine()
    cnt = engine.repo.get_by_id(container_id)
    if not cnt:
        flash("Container not found.", "warning")
        return redirect(url_for("containers.index"))

    return render_template("containers/detail.html", container=cnt)

@containers_bp.route("/<container_id>/start", methods=["POST"])
def start(container_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_container_engine()
    success, msg = engine.start_container(container_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("containers.index"))

@containers_bp.route("/<container_id>/stop", methods=["POST"])
def stop(container_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_container_engine()
    success, msg = engine.stop_container(container_id)
    flash(msg, "info" if success else "danger")
    return redirect(url_for("containers.index"))

@containers_bp.route("/<container_id>/restart", methods=["POST"])
def restart(container_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_container_engine()
    success, msg = engine.restart_container(container_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("containers.index"))
