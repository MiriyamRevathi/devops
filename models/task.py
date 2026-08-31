from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class TaskItem:
    """Domain model for a DevOps task card on the Kanban board."""

    COL_BACKLOG = "Backlog"
    COL_READY = "Ready"
    COL_IN_PROGRESS = "In Progress"
    COL_REVIEW = "Review"
    COL_DONE = "Done"

    COLUMNS = [COL_BACKLOG, COL_READY, COL_IN_PROGRESS, COL_REVIEW, COL_DONE]

    def __init__(
        self,
        title: str,
        description: str,
        assignee: str = "unassigned",
        priority: str = "Medium",
        column: str = COL_BACKLOG,
        task_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
        due_date: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = task_id or generate_id("tsk")
        self.title = title
        self.description = description
        self.assignee = assignee
        self.priority = priority
        self.column = column
        self.labels = labels or ["devops"]
        self.due_date = due_date or "2026-09-15"
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "priority": self.priority,
            "column": self.column,
            "labels": self.labels,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskItem":
        return cls(
            task_id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            assignee=data.get("assignee", "unassigned"),
            priority=data.get("priority", "Medium"),
            column=data.get("column", cls.COL_BACKLOG),
            labels=data.get("labels", []),
            due_date=data.get("due_date"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
