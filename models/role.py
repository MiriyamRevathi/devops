from typing import List, Dict, Any

class Role:
    """Role definition and permission mapping."""
    ADMIN = "Admin"
    DEVOPS = "DevOps Engineer"
    DEVELOPER = "Developer"
    QA = "QA Engineer"
    VIEWER = "Viewer"

    ALL_ROLES = [ADMIN, DEVOPS, DEVELOPER, QA, VIEWER]

    PERMISSIONS = {
        ADMIN: ["read", "write", "delete", "execute_pipelines", "deploy", "manage_users", "manage_teams", "approve_changes", "manage_infrastructure"],
        DEVOPS: ["read", "write", "execute_pipelines", "deploy", "manage_teams", "approve_changes", "manage_infrastructure"],
        DEVELOPER: ["read", "write", "execute_pipelines", "create_pr", "create_change"],
        QA: ["read", "write", "execute_pipelines", "trigger_tests", "create_incident"],
        VIEWER: ["read"]
    }

    @classmethod
    def get_permissions(cls, role_name: str) -> List[str]:
        return cls.PERMISSIONS.get(role_name, ["read"])

    @classmethod
    def has_permission(cls, role_name: str, permission: str) -> bool:
        return permission in cls.get_permissions(role_name)
