from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.user import User
from core.security import SecurityManager

class UserRepository:
    """Repository handling local User data persistence and seed demo accounts."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "users.json")
        self._seed_default_users()

    def _seed_default_users(self) -> None:
        if self.store.count() == 0:
            demo_users = [
                User(
                    username="admin",
                    email="admin@devopsflow.local",
                    password_hash=SecurityManager.hash_password("admin123"),
                    role="Admin",
                    full_name="Platform Admin"
                ),
                User(
                    username="devops",
                    email="devops@devopsflow.local",
                    password_hash=SecurityManager.hash_password("devops123"),
                    role="DevOps Engineer",
                    full_name="Lead DevOps Engineer"
                ),
                User(
                    username="developer",
                    email="developer@devopsflow.local",
                    password_hash=SecurityManager.hash_password("dev123"),
                    role="Developer",
                    full_name="Senior Software Developer"
                ),
                User(
                    username="qa",
                    email="qa@devopsflow.local",
                    password_hash=SecurityManager.hash_password("qa123"),
                    role="QA Engineer",
                    full_name="QA Lead"
                ),
                User(
                    username="viewer",
                    email="viewer@devopsflow.local",
                    password_hash=SecurityManager.hash_password("viewer123"),
                    role="Viewer",
                    full_name="Guest Viewer"
                )
            ]
            for user in demo_users:
                self.store.insert(user.to_dict())

    def get_by_id(self, user_id: str) -> Optional[User]:
        data = self.store.find_by_id(user_id)
        return User.from_dict(data) if data else None

    def get_by_username(self, username: str) -> Optional[User]:
        results = self.store.find_where(lambda u: u.get("username", "").lower() == username.lower().strip())
        return User.from_dict(results[0]) if results else None

    def get_by_email(self, email: str) -> Optional[User]:
        results = self.store.find_where(lambda u: u.get("email", "").lower() == email.lower().strip())
        return User.from_dict(results[0]) if results else None

    def get_all(self) -> List[User]:
        return [User.from_dict(d) for d in self.store.read_all()]

    def create(self, user: User) -> User:
        self.store.insert(user.to_dict())
        return user

    def update(self, user: User) -> Optional[User]:
        updated = self.store.update(user.id, user.to_dict())
        return User.from_dict(updated) if updated else None

    def delete(self, user_id: str) -> bool:
        return self.store.delete(user_id)
