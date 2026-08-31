from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.team_service import TeamService
from repositories.team_repo import TeamRepository

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")

def get_team_service() -> TeamService:
    repo = TeamRepository(current_app.config["TEAMS_DATA_DIR"])
    return TeamService(repo)

@teams_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_team_service()
    teams = service.repo.get_all()
    return render_template("teams/list.html", teams=teams)

@teams_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        lead = request.form.get("lead", session.get("username", "admin")).strip()

        service = get_team_service()
        success, team, msg = service.create_team(name=name, description=description, lead=lead)

        if success and team:
            flash(msg, "success")
            return redirect(url_for("teams.index"))
        else:
            flash(msg, "danger")

    return render_template("teams/create.html")
