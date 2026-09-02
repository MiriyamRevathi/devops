from typing import Tuple, Optional, List, Dict, Any
from repositories.task_repo import TaskRepository
from models.task import TaskItem
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class TaskBoardService:
    """DevOps Task Kanban board service."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = TaskRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def create_task(
        self,
        title: str,
        description: str,
        assignee: str = "unassigned",
        priority: str = "Medium",
        column: str = TaskItem.COL_BACKLOG,
        due_date: str = "2026-09-15"
    ) -> Tuple[bool, Optional[TaskItem], str]:
        if not title:
            return False, None, "Task title is required."

        task = TaskItem(
            title=title.strip(),
            description=description.strip(),
            assignee=assignee,
            priority=priority,
            column=column,
            due_date=due_date
        )

        saved = self.repo.save(task)
        EventBus.publish("task_created", task_id=saved.id, title=saved.title)
        return True, saved, "Task created successfully."

    def move_task_status(self, task_id: str, new_column: str) -> Tuple[bool, str]:
        task = self.repo.get_by_id(task_id)
        if not task:
            return False, "Task not found."

        if new_column not in TaskItem.COLUMNS:
            return False, "Invalid column target."

        task.column = new_column
        task.updated_at = get_utc_now_iso()
        self.repo.save(task)
        EventBus.publish("task_moved", task_id=task_id, column=new_column)
        return True, f"Task moved to {new_column}."
