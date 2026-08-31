"""
Domain entity models and data structures for source_control.
Calculates validation rules, state transitions, and serialization.
"""
from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class SourceControlEntity:
    """Domain model for source_control entity."""
    def __init__(self, name: str, description: str = "", entity_id: Optional[str] = None, status: str = "ACTIVE", metadata: Optional[Dict[str, Any]] = None):
        self.id = entity_id or generate_id("sou")
        self.name = name
        self.description = description
        self.status = status
        self.metadata = metadata or {}
        self.created_at = get_utc_now_iso()
        self.updated_at = get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def validate(self) -> bool:
        return bool(self.name and len(self.name.strip()) >= 2)
