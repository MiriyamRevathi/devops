from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.artifact_service import ArtifactService
from repositories.artifact_repo import ArtifactRepository

artifacts_bp = Blueprint("artifacts", __name__, url_prefix="/artifacts")

def get_artifact_service() -> ArtifactService:
    repo = ArtifactRepository(current_app.config["ARTIFACTS_DATA_DIR"])
    return ArtifactService(repo)

@artifacts_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_artifact_service()
    artifacts = service.repo.get_all()
    return render_template("artifacts/list.html", artifacts=artifacts)

@artifacts_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        version = request.form.get("version", "").strip()
        art_type = request.form.get("artifact_type", "wheel").strip()
        size_bytes = int(request.form.get("size_bytes", 1048576))
        created_by = session.get("username", "admin")

        service = get_artifact_service()
        success, art, msg = service.register_artifact(
            name=name,
            version=version,
            artifact_type=art_type,
            size_bytes=size_bytes,
            created_by=created_by
        )

        if success:
            flash(msg, "success")
            return redirect(url_for("artifacts.index"))
        else:
            flash(msg, "danger")

    return render_template("artifacts/register.html")

@artifacts_bp.route("/<artifact_id>/delete", methods=["POST"])
def delete(artifact_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_artifact_service()
    success, msg = service.delete_artifact(artifact_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("artifacts.index"))
