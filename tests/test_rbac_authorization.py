import pytest
from core.factory import create_app
from core.security import SecurityManager
from config import Config

@pytest.fixture
def app():
    app = create_app("testing")
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def login_as(client, username, role="Viewer"):
    with client.session_transaction() as sess:
        sess["user_id"] = f"user_{username}"
        sess["username"] = username
        sess["role"] = role
        sess["full_name"] = f"Test {username.capitalize()}"

def test_five_roles_permissions_matrix():
    # Admin has all permissions
    assert SecurityManager.has_permission("Admin", "user.manage") is True
    assert SecurityManager.has_permission("Admin", "deployment.production") is True

    # DevOps Engineer
    assert SecurityManager.has_permission("DevOps Engineer", "deployment.production") is True
    assert SecurityManager.has_permission("DevOps Engineer", "infrastructure.destroy") is True
    assert SecurityManager.has_permission("DevOps Engineer", "user.manage") is False
    assert SecurityManager.has_permission("DevOps Engineer", "settings.manage") is False

    # Developer
    assert SecurityManager.has_permission("Developer", "project.create") is True
    assert SecurityManager.has_permission("Developer", "pull_request.create") is True
    assert SecurityManager.has_permission("Developer", "deployment.production") is False
    assert SecurityManager.has_permission("Developer", "user.manage") is False

    # QA Engineer
    assert SecurityManager.has_permission("QA Engineer", "testing.view") is True
    assert SecurityManager.has_permission("QA Engineer", "testing.run") is True
    assert SecurityManager.has_permission("QA Engineer", "deployment.production") is False
    assert SecurityManager.has_permission("QA Engineer", "infrastructure.apply") is False

    # Viewer (Read-only)
    assert SecurityManager.has_permission("Viewer", "project.view") is True
    assert SecurityManager.has_permission("Viewer", "project.create") is False
    assert SecurityManager.has_permission("Viewer", "pipeline.run") is False
    assert SecurityManager.has_permission("Viewer", "deployment.create") is False

def test_admin_full_access(client):
    login_as(client, "admin", "Admin")
    res_users = client.get("/users/")
    assert res_users.status_code == 200

    res_settings = client.get("/settings/")
    assert res_settings.status_code == 200

def test_devops_engineer_restricted_urls(client):
    login_as(client, "devops", "DevOps Engineer")

    # Allowed routes
    assert client.get("/deployments/").status_code == 200
    assert client.get("/infrastructure/").status_code == 200

    # Restricted routes -> 403 Forbidden
    res_users = client.get("/users/")
    assert res_users.status_code == 403

    res_settings = client.get("/settings/")
    assert res_settings.status_code == 403

def test_developer_restricted_production_deployment(client):
    login_as(client, "developer", "Developer")

    # Allowed routes
    assert client.get("/projects/").status_code == 200
    assert client.get("/pipelines/builds").status_code == 200

    # Restricted User Management -> 403
    assert client.get("/users/").status_code == 403

    # Restricted Production Deployment -> 403
    post_prod = client.post("/deployments/deploy", data={
        "project_id": "PROJ-101",
        "environment": "Production",
        "version": "v1.4.0",
        "commit_hash": "a1b2c3d4"
    })
    assert post_prod.status_code == 403

def test_qa_engineer_testing_dashboard_and_restrictions(client):
    login_as(client, "qa", "QA Engineer")

    # QA Dedicated Testing Page -> 200 OK
    res_testing = client.get("/testing/")
    assert res_testing.status_code == 200

    # Restricted Production Deployment -> 403
    post_prod = client.post("/deployments/deploy", data={
        "project_id": "PROJ-101",
        "environment": "Production",
        "version": "v1.4.0"
    })
    assert post_prod.status_code == 403

    # Restricted Infrastructure Destroy -> 403
    post_infra = client.post("/infrastructure/plans/plan-1/destroy")
    assert post_infra.status_code == 403

def test_viewer_read_only_enforcement(client):
    login_as(client, "viewer", "Viewer")

    # Viewing routes -> 200 OK
    assert client.get("/").status_code == 200
    assert client.get("/projects/").status_code == 200
    assert client.get("/pipelines/").status_code == 200
    assert client.get("/deployments/").status_code == 200

    # Any mutation -> 403 Forbidden
    assert client.post("/projects/create", data={"name": "Illegal", "key": "ILL"}).status_code == 403
    assert client.post("/pipelines/pipe-1/run").status_code == 403
    assert client.post("/containers/create", data={"name": "c1", "image": "img"}).status_code == 403
