"""
Service layer for artifacts operations.
"""
from typing import Tuple, Optional, List, Dict, Any
from storage.json_store import JSONStore
from core.events import EventBus

class ArtifactsDomainService:
    """Service managing artifacts domain operations."""
    def __init__(self, data_dir: str):
        self.store = JSONStore(data_dir, "artifacts_entities.json")

    def create_entity(self, name: str, description: str = "") -> Tuple[bool, Optional[Dict[str, Any]], str]:
        if not name:
            return False, None, "Name is required."
        record = {"id": name.lower().replace(" ", "_"), "name": name, "description": description, "status": "ACTIVE"}
        self.store.insert(record)
        EventBus.publish("artifacts_entity_created", entity_id=record["id"])
        return True, record, "Created successfully."

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.read_all()
