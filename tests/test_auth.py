import pytest
import shutil
import tempfile
from pathlib import Path
from models.user import User
from models.role import Role
from repositories.user_repo import UserRepository
from services.auth_service import AuthService
from core.security import SecurityManager

@pytest.fixture
def temp_user_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_user_model():
    pwd_hash = SecurityManager.hash_password("secret123")
    user = User(
        username="johndoe",
        email="john@example.com",
        password_hash=pwd_hash,
        role="Developer",
        full_name="John Doe"
    )
    assert user.username == "johndoe"
    assert user.check_password("secret123") is True
    assert user.check_password("wrongpass") is False
    assert user.is_admin() is False

def test_user_repository(temp_user_dir):
    repo = UserRepository(temp_user_dir)
    # Default seed users should exist
    users = repo.get_all()
    assert len(users) >= 5
    
    admin = repo.get_by_username("admin")
    assert admin is not None
    assert admin.role == "Admin"

def test_auth_service_authentication(temp_user_dir):
    repo = UserRepository(temp_user_dir)
    service = AuthService(repo)

    success, user, msg = service.authenticate("admin", "admin123")
    assert success is True
    assert user is not None
    assert user.username == "admin"

    fail_success, fail_user, fail_msg = service.authenticate("admin", "wrongpass")
    assert fail_success is False
    assert fail_user is None

def test_auth_service_registration(temp_user_dir):
    repo = UserRepository(temp_user_dir)
    service = AuthService(repo)

    success, new_user, msg = service.register_user(
        username="newdev",
        email="newdev@example.com",
        password="password123",
        role="Developer",
        full_name="New Developer"
    )
    assert success is True
    assert new_user is not None
    assert new_user.username == "newdev"

    # Duplicate username check
    dup_success, _, _ = service.register_user("newdev", "other@example.com", "pass123")
    assert dup_success is False

def test_role_permissions():
    assert Role.has_permission(Role.ADMIN, "manage_users") is True
    assert Role.has_permission(Role.VIEWER, "delete") is False
    assert Role.has_permission(Role.DEVELOPER, "create_pr") is True
