from typing import Tuple, Optional, List, Dict, Any
from repositories.change_repo import ChangeRepository
from models.change import ChangeRequest
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class ChangeManagementService:
    """Change Advisory Board (CAB) Workflow Engine."""

    def __init__(self, repository: ChangeRepository):
        self.repo = repository

    def create_change_request(
        self,
        title: str,
        description: str,
        affected_services: str,
        risk_level: str = "MEDIUM",
        impact: str = "MODERATE",
        rollback_plan: str = "",
        requester: str = "admin"
    ) -> Tuple[bool, Optional[ChangeRequest], str]:
        if not title:
            return False, None, "Title is required."

        chg = ChangeRequest(
            title=title.strip(),
            description=description.strip(),
            affected_services=affected_services.strip(),
            risk_level=risk_level,
            impact=impact,
            rollback_plan=rollback_plan.strip(),
            requester=requester,
            status=ChangeRequest.STATUS_SUBMITTED
        )

        saved = self.repo.save(chg)
        EventBus.publish("change_request_submitted", change_id=saved.id, title=saved.title)
        return True, saved, "Change request submitted for review."

    def advance_status(self, change_id: str, actor: str) -> Tuple[bool, str]:
        chg = self.repo.get_by_id(change_id)
        if not chg:
            return False, "Change request not found."

        idx = ChangeRequest.WORKFLOW.index(chg.status) if chg.status in ChangeRequest.WORKFLOW else 0
        if idx >= len(ChangeRequest.WORKFLOW) - 1:
            return False, "Change request is already closed."

        new_status = ChangeRequest.WORKFLOW[idx + 1]
        chg.status = new_status
        if new_status == ChangeRequest.STATUS_APPROVED:
            if actor not in chg.approvers:
                chg.approvers.append(actor)

        chg.updated_at = get_utc_now_iso()
        self.repo.save(chg)
        EventBus.publish("change_status_advanced", change_id=change_id, status=new_status)
        return True, f"Change status advanced to {new_status}."
