from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.team_service import TeamService
from services.audit_service import AuditService
from models.team import Team

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")

def get_team_service() -> TeamService:
    return TeamService(current_app.config["TEAMS_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@teams_bp.route("/", methods=["GET"])
@login_required
@permission_required("team.manage")
def list_teams():
    service = get_team_service()
    teams = service.get_all_teams()
    return render_template("teams/list.html", teams=teams)

@teams_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("team.manage")
def create():
    if request.method == "POST":
        name = SecurityManager.sanitize_input(request.form.get("name", ""))
        lead = SecurityManager.sanitize_input(request.form.get("lead", "devops"))
        description = SecurityManager.sanitize_input(request.form.get("description", ""))

        if not name:
            flash("Team Name is required.", "danger")
            return render_template("teams/create.html")

        service = get_team_service()
        t = Team(name=name, lead=lead, description=description)
        service.create_team(t)

        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="TEAM_CREATED",
            resource=f"Team:{t.name}",
            details=f"Created team '{name}' with lead '{lead}'."
        )

        flash(f"Team '{name}' created successfully.", "success")
        return redirect(url_for("teams.list_teams"))

    return render_template("teams/create.html")
