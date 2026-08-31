from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.repository_service import RepositoryService
from repositories.source_control_repo import SourceControlRepository

repositories_bp = Blueprint("repositories", __name__, url_prefix="/repositories")

def get_repo_service() -> RepositoryService:
    repo_store = SourceControlRepository(current_app.config["REPOSITORIES_DATA_DIR"])
    return RepositoryService(repo_store)

@repositories_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_repo_service()
    repos = service.repo_store.get_all()
    return render_template("repositories/list.html", repositories=repos)

@repositories_bp.route("/<repo_id>")
def detail(repo_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_repo_service()
    repo = service.repo_store.get_by_id(repo_id)
    if not repo:
        flash("Repository not found.", "warning")
        return redirect(url_for("repositories.index"))

    return render_template("repositories/detail.html", repository=repo)

@repositories_bp.route("/<repo_id>/branches", methods=["POST"])
def create_branch(repo_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    branch_name = request.form.get("branch_name", "").strip()
    from_branch = request.form.get("from_branch", "main").strip()

    service = get_repo_service()
    success, message = service.create_branch(repo_id, branch_name, from_branch)

    flash(message, "success" if success else "danger")
    return redirect(url_for("repositories.detail", repo_id=repo_id))

@repositories_bp.route("/<repo_id>/commits", methods=["GET", "POST"])
def commits(repo_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_repo_service()
    repo = service.repo_store.get_by_id(repo_id)
    if not repo:
        flash("Repository not found.", "warning")
        return redirect(url_for("repositories.index"))

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        branch_name = request.form.get("branch", "main").strip()
        files = request.form.get("files", "src/index.js").split(",")
        author = session.get("username", "admin")

        success, commit, msg = service.commit_changes(
            repo_id=repo_id,
            branch_name=branch_name,
            message=message,
            author=author,
            changed_files=[f.strip() for f in files if f.strip()]
        )
        flash(msg, "success" if success else "danger")
        return redirect(url_for("repositories.commits", repo_id=repo_id))

    return render_template("repositories/commits.html", repository=repo)

@repositories_bp.route("/<repo_id>/pull-requests", methods=["GET", "POST"])
def pull_requests(repo_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_repo_service()
    repo = service.repo_store.get_by_id(repo_id)
    if not repo:
        flash("Repository not found.", "warning")
        return redirect(url_for("repositories.index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        source_branch = request.form.get("source_branch", "").strip()
        target_branch = request.form.get("target_branch", "main").strip()
        author = session.get("username", "admin")

        success, pr, msg = service.create_pull_request(
            repo_id=repo_id,
            title=title,
            description=description,
            author=author,
            source_branch=source_branch,
            target_branch=target_branch
        )
        flash(msg, "success" if success else "danger")
        return redirect(url_for("repositories.pull_requests", repo_id=repo_id))

    return render_template("repositories/pull_requests.html", repository=repo)

@repositories_bp.route("/<repo_id>/pull-requests/<pr_id>/merge", methods=["POST"])
def merge_pr(repo_id: str, pr_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    merger = session.get("username", "admin")
    service = get_repo_service()
    success, message = service.merge_pull_request(repo_id, pr_id, merger)

    flash(message, "success" if success else "danger")
    return redirect(url_for("repositories.pull_requests", repo_id=repo_id))
