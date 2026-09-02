from typing import Tuple, Optional, Dict, Any, List
from repositories.user_repo import UserRepository
from models.user import User
from models.role import Role
from core.security import SecurityManager
from utils.validators import DataValidator
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class AuthService:
    """Authentication and Role-Based Access Control (RBAC) service engine."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = UserRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        if not username or not password:
            return False, None, "Username and password are required."

        user = self.repo.get_by_username(username)
        if not user:
            return False, None, "Invalid username or password."

        if not user.is_active:
            return False, None, "Account is disabled."

        if not user.check_password(password):
            return False, None, "Invalid username or password."

        user.last_login = get_utc_now_iso()
        self.repo.update(user)

        EventBus.publish("user_logged_in", user_id=user.id, username=user.username)
        return True, user, "Login successful."

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        role: str = "Developer",
        full_name: str = ""
    ) -> Tuple[bool, Optional[User], str]:
        username = SecurityManager.sanitize_input(username)
        email = SecurityManager.sanitize_input(email)
        
        if not username or len(username) < 3:
            return False, None, "Username must be at least 3 characters long."

        if not DataValidator.validate_email(email):
            return False, None, "Invalid email address format."

        if not password or len(password) < 6:
            return False, None, "Password must be at least 6 characters long."

        if self.repo.get_by_username(username):
            return False, None, "Username is already taken."

        if self.repo.get_by_email(email):
            return False, None, "Email address is already registered."

        if role not in Role.ALL_ROLES:
            role = "Developer"

        pwd_hash = SecurityManager.hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=pwd_hash,
            role=role,
            full_name=full_name or username
        )

        created_user = self.repo.create(new_user)
        EventBus.publish("user_registered", user_id=created_user.id, username=created_user.username)
        return True, created_user, "User registered successfully."

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def get_all_users(self) -> List[User]:
        return self.repo.get_all()

    def check_user_permission(self, user: Optional[User], permission: str) -> bool:
        if not user:
            return False
        return Role.has_permission(user.role, permission)
