from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.task import TaskItem

class TaskRepository:
    """Repository handling Kanban board Task persistence and seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "tasks.json")
        self._seed_default_tasks()

    def _seed_default_tasks(self) -> None:
        if self.store.count() == 0:
            defaults = [
                TaskItem("Upgrade Kubernetes Cluster Helm charts", "Migrate Helm v2 templates to Helm v3", "devops", "High", TaskItem.COL_IN_PROGRESS),
                TaskItem("Configure Prometheus alert rules for DB latency", "Set threshold for 95th percentile response time", "admin", "Medium", TaskItem.COL_READY),
                TaskItem("Audit IAM role permissions for CI runner service account", "Enforce least privilege access model", "developer", "High", TaskItem.COL_REVIEW),
                TaskItem("Implement automated database backup verification script", "Daily dry-run restore tests", "devops", "Low", TaskItem.COL_DONE)
            ]
            for t in defaults:
                self.store.insert(t.to_dict())

    def get_by_id(self, task_id: str) -> Optional[TaskItem]:
        data = self.store.find_by_id(task_id)
        return TaskItem.from_dict(data) if data else None

    def get_all(self) -> List[TaskItem]:
        return [TaskItem.from_dict(r) for r in self.store.read_all()]

    def save(self, task: TaskItem) -> TaskItem:
        existing = self.get_by_id(task.id)
        if existing:
            self.store.update(task.id, task.to_dict())
        else:
            self.store.insert(task.to_dict())
        return task

    def delete(self, task_id: str) -> bool:
        return self.store.delete(task_id)
