"""
Lifecycle Service for audit domain entity management.
Manages resource instantiation, state updates, validation, and storage persistence.
"""
from typing import Dict, Any, List, Optional, Tuple
from utils.helpers import get_utc_now_iso, generate_id
from storage.json_store import JSONStore
from core.events import EventBus

class AuditLifecycleService:
    """Manages lifecycle state, persistence, and event triggers for audit."""
    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "audit_lifecycle.json")

    def create(self, name: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        if not name or len(name.strip()) < 2:
            return False, None, "Name must be at least 2 characters long."
        
        record = {
            "id": generate_id("lc_aud"),
            "name": name.strip(),
            "status": "INITIALIZED",
            "payload": payload or {},
            "created_at": get_utc_now_iso(),
            "updated_at": get_utc_now_iso()
        }
        
        self.store.insert(record)
        EventBus.publish("audit_lifecycle_created", record_id=record["id"])
        return True, record, "Created successfully."

    def update_status(self, record_id: str, new_status: str) -> Tuple[bool, str]:
        record = self.store.find_by_id(record_id)
        if not record:
            return False, "Record not found."
        
        record["status"] = new_status
        record["updated_at"] = get_utc_now_iso()
        self.store.update(record_id, record)
        EventBus.publish("audit_lifecycle_status_updated", record_id=record_id, status=new_status)
        return True, f"Status updated to {new_status}."

    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        return self.store.find_by_id(record_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.read_all()
