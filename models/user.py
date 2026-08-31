from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id
from core.security import SecurityManager

class User:
    """User domain model for DevOpsFlow local authentication & RBAC system."""

    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        role: str = "Developer",
        full_name: str = "",
        user_id: Optional[str] = None,
        is_active: bool = True,
        team_ids: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        last_login: Optional[str] = None
    ):
        self.id = user_id or generate_id("usr")
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.full_name = full_name or username
        self.is_active = is_active
        self.team_ids = team_ids or []
        self.created_at = created_at or get_utc_now_iso()
        self.last_login = last_login

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "team_ids": self.team_ids,
            "created_at": self.created_at,
            "last_login": self.last_login
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            user_id=data.get("id"),
            username=data.get("username", ""),
            email=data.get("email", ""),
            password_hash=data.get("password_hash", ""),
            role=data.get("role", "Developer"),
            full_name=data.get("full_name", ""),
            is_active=data.get("is_active", True),
            team_ids=data.get("team_ids", []),
            created_at=data.get("created_at"),
            last_login=data.get("last_login")
        )

    def check_password(self, password: str) -> bool:
        return SecurityManager.verify_password(password, self.password_hash)

    def is_admin(self) -> bool:
        return self.role == "Admin"
