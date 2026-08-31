from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso

class ProjectSettings:
    def __init__(
        self,
        project_id: str,
        auto_deploy_staging: bool = True,
        auto_deploy_production: bool = False,
        require_pr_review: bool = True,
        minimum_reviewers: int = 1,
        allowed_environments: Optional[List[str]] = None,
        notification_channel: str = "#devops-alerts"
    ):
        self.project_id = project_id
        self.auto_deploy_staging = auto_deploy_staging
        self.auto_deploy_production = auto_deploy_production
        self.require_pr_review = require_pr_review
        self.minimum_reviewers = minimum_reviewers
        self.allowed_environments = allowed_environments or ["Development", "Testing", "Staging", "Production"]
        self.notification_channel = notification_channel
        self.updated_at = get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "auto_deploy_staging": self.auto_deploy_staging,
            "auto_deploy_production": self.auto_deploy_production,
            "require_pr_review": self.require_pr_review,
            "minimum_reviewers": self.minimum_reviewers,
            "allowed_environments": self.allowed_environments,
            "notification_channel": self.notification_channel,
            "updated_at": self.updated_at
        }
