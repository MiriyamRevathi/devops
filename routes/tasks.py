from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.task_board_service import TaskBoardService
from repositories.task_repo import TaskRepository
from models.task import TaskItem

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def get_task_service() -> TaskBoardService:
    repo = TaskRepository(current_app.config["TASKS_DATA_DIR"])
    return TaskBoardService(repo)

@tasks_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    service = get_task_service()
    all_tasks = service.repo.get_all()

    # Group by column
    board = {col: [] for col in TaskItem.COLUMNS}
    for t in all_tasks:
        if t.column in board:
            board[t.column].append(t)
        else:
            board[TaskItem.COL_BACKLOG].append(t)

    return render_template("tasks/board.html", board=board, columns=TaskItem.COLUMNS)

@tasks_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        assignee = request.form.get("assignee", session.get("username", "admin")).strip()
        priority = request.form.get("priority", "Medium").strip()
        column = request.form.get("column", TaskItem.COL_BACKLOG).strip()

        service = get_task_service()
        success, task, msg = service.create_task(
            title=title,
            description=description,
            assignee=assignee,
            priority=priority,
            column=column
        )

        if success:
            flash(msg, "success")
            return redirect(url_for("tasks.index"))
        else:
            flash(msg, "danger")

    return render_template("tasks/create.html", columns=TaskItem.COLUMNS)

@tasks_bp.route("/<task_id>/move", methods=["POST"])
def move(task_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    new_column = request.form.get("column", TaskItem.COL_BACKLOG).strip()
    service = get_task_service()
    success, msg = service.move_task_status(task_id, new_column)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": success, "message": msg})

    flash(msg, "success" if success else "danger")
    return redirect(url_for("tasks.index"))
