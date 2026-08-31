from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.change_management_service import ChangeManagementService
from repositories.change_repo import ChangeRepository

changes_bp = Blueprint("changes", __name__, url_prefix="/changes")

def get_change_service() -> ChangeManagementService:
    repo = ChangeRepository(current_app.config["CHANGES_DATA_DIR"])
    return ChangeManagementService(repo)

@changes_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_change_service()
    requests_list = service.repo.get_all()
    return render_template("changes/list.html", requests=requests_list)

@changes_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        affected_services = request.form.get("affected_services", "").strip()
        risk_level = request.form.get("risk_level", "MEDIUM").strip()
        impact = request.form.get("impact", "MODERATE").strip()
        rollback_plan = request.form.get("rollback_plan", "").strip()
        requester = session.get("username", "admin")

        service = get_change_service()
        success, chg, msg = service.create_change_request(
            title=title,
            description=description,
            affected_services=affected_services,
            risk_level=risk_level,
            impact=impact,
            rollback_plan=rollback_plan,
            requester=requester
        )

        if success and chg:
            flash(msg, "success")
            return redirect(url_for("changes.detail", change_id=chg.id))
        else:
            flash(msg, "danger")

    return render_template("changes/create.html")

@changes_bp.route("/<change_id>")
def detail(change_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_change_service()
    chg = service.repo.get_by_id(change_id)
    if not chg:
        flash("Change request not found.", "warning")
        return redirect(url_for("changes.index"))

    return render_template("changes/detail.html", change=chg)

@changes_bp.route("/<change_id>/advance", methods=["POST"])
def advance(change_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    actor = session.get("username", "admin")
    service = get_change_service()
    success, msg = service.advance_status(change_id, actor=actor)

    flash(msg, "success" if success else "danger")
    return redirect(url_for("changes.detail", change_id=change_id))
