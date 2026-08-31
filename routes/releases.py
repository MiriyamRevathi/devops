from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.deployment_service import DeploymentService
from repositories.deployment_repo import DeploymentRepository

releases_bp = Blueprint("releases", __name__, url_prefix="/releases")

def get_release_service() -> DeploymentService:
    repo = DeploymentRepository(current_app.config["RELEASES_DATA_DIR"])
    return DeploymentService(repo)

@releases_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_release_service()
    releases = service.repo.get_all_releases()
    return render_template("releases/list.html", releases=releases)

@releases_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        version_tag = request.form.get("version_tag", "").strip()
        title = request.form.get("title", "").strip()
        release_notes = request.form.get("release_notes", "").strip()
        project_id = request.form.get("project_id", "proj_default").strip()
        targets = request.form.getlist("targets")
        author = session.get("username", "admin")

        service = get_release_service()
        success, release, msg = service.create_release(
            version_tag=version_tag,
            project_id=project_id,
            title=title,
            release_notes=release_notes,
            author=author,
            deployment_targets=targets
        )

        if success and release:
            flash(msg, "success")
            return redirect(url_for("releases.detail", release_id=release.id))
        else:
            flash(msg, "danger")

    return render_template("releases/create.html")

@releases_bp.route("/<release_id>")
def detail(release_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_release_service()
    rel = service.repo.get_release_by_id(release_id)
    if not rel:
        flash("Release not found.", "warning")
        return redirect(url_for("releases.index"))

    return render_template("releases/detail.html", release=rel)
