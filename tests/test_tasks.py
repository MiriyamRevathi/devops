import pytest
import shutil
import tempfile
from models.task import TaskItem
from repositories.task_repo import TaskRepository
from services.task_board_service import TaskBoardService

@pytest.fixture
def temp_task_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_task_kanban_service(temp_task_dir):
    repo = TaskRepository(temp_task_dir)
    service = TaskBoardService(repo)

    tasks = repo.get_all()
    assert len(tasks) >= 4

    success, task, msg = service.create_task("Fix CI pipeline timeout", "Increase step timeout to 10 mins", "devops")
    assert success is True
    assert task is not None
    assert task.column == TaskItem.COL_BACKLOG

    move_success, move_msg = service.move_task_status(task.id, TaskItem.COL_IN_PROGRESS)
    assert move_success is True
    assert repo.get_by_id(task.id).column == TaskItem.COL_IN_PROGRESS
