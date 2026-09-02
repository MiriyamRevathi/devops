from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.repository_service import RepositoryService
from services.audit_service import AuditService

repositories_bp = Blueprint("repositories", __name__)

def get_repo_service() -> RepositoryService:
    return RepositoryService(current_app.config["REPOSITORIES_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@repositories_bp.route("/repositories", methods=["GET"])
@repositories_bp.route("/git", methods=["GET"])
@login_required
@permission_required("git.view")
def list_repositories():
    service = get_repo_service()
    repos = service.get_all_repositories()
    return render_template("repositories/list.html", repositories=repos)

@repositories_bp.route("/repositories/index", methods=["GET"])
@login_required
@permission_required("git.view")
def index():
    return list_repositories()

@repositories_bp.route("/repositories/<repo_id>", methods=["GET"])
@login_required
@permission_required("git.view")
def detail(repo_id: str):
    service = get_repo_service()
    repo = service.get_repository_by_id(repo_id)
    if not repo:
        flash("Repository not found.", "danger")
        return redirect(url_for("repositories.list_repositories"))
    return render_template("repositories/detail.html", repo=repo)

@repositories_bp.route("/repositories/<repo_id>/commits", methods=["GET"])
@login_required
@permission_required("git.view")
def commits(repo_id: str):
    service = get_repo_service()
    repo = service.get_repository_by_id(repo_id)
    if not repo:
        flash("Repository not found.", "danger")
        return redirect(url_for("repositories.list_repositories"))
    return render_template("repositories/commits.html", repo=repo)

@repositories_bp.route("/repositories/<repo_id>/branches/create", methods=["POST"])
@login_required
@permission_required("git.branch.create")
def create_branch(repo_id: str):
    branch_name = SecurityManager.sanitize_input(request.form.get("branch_name", ""))
    service = get_repo_service()
    if branch_name and service.add_branch(repo_id, branch_name):
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="BRANCH_CREATED",
            resource=f"Repo:{repo_id}",
            details=f"Created branch '{branch_name}'."
        )
        flash(f"Branch '{branch_name}' created.", "success")
    else:
        flash("Failed to create branch or branch already exists.", "danger")
    return redirect(url_for("repositories.detail", repo_id=repo_id))

@repositories_bp.route("/pull-requests", methods=["GET"])
@repositories_bp.route("/repositories/<repo_id>/pull-requests", methods=["GET"])
@login_required
@permission_required("git.view")
def pull_requests(repo_id: str = None):
    service = get_repo_service()
    if repo_id:
        repo = service.get_repository_by_id(repo_id)
        repos = [repo] if repo else []
    else:
        repos = service.get_all_repositories()

    all_prs = []
    for r in repos:
        if r and hasattr(r, 'pull_requests'):
            for pr in r.pull_requests:
                all_prs.append({"repo": r, "pr": pr})

    return render_template("repositories/pull_requests.html", pull_requests=all_prs, current_repo_id=repo_id)

@repositories_bp.route("/repositories/<repo_id>/pull-requests/create", methods=["POST"])
@login_required
@permission_required("pull_request.create")
def create_pull_request(repo_id: str):
    title = SecurityManager.sanitize_input(request.form.get("title", ""))
    source_branch = request.form.get("source_branch", "feature")
    target_branch = request.form.get("target_branch", "main")
    author = session.get("username", "developer")

    service = get_repo_service()
    pr = service.create_pull_request(repo_id, title, source_branch, target_branch, author)
    if pr:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="PR_CREATED",
            resource=f"Repo:{repo_id}",
            details=f"Created Pull Request #{pr.id}: '{title}' ({source_branch} -> {target_branch})."
        )
        flash(f"Pull Request #{pr.id} created.", "success")
    else:
        flash("Failed to create Pull Request.", "danger")
    return redirect(url_for("repositories.pull_requests", repo_id=repo_id))

@repositories_bp.route("/repositories/<repo_id>/pull-requests/<pr_id>/merge", methods=["POST"])
@login_required
@permission_required("pull_request.merge")
def merge_pull_request(repo_id: str, pr_id: str):
    service = get_repo_service()
    if service.merge_pull_request(repo_id, pr_id):
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="PR_MERGED",
            resource=f"Repo:{repo_id}",
            details=f"Merged Pull Request #{pr_id} into target branch."
        )
        flash(f"Pull Request #{pr_id} merged successfully.", "success")
    else:
        flash("Failed to merge Pull Request.", "danger")
    return redirect(url_for("repositories.pull_requests", repo_id=repo_id))
