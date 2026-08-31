import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

class JSONStore:
    """Thread-safe JSON file storage engine supporting indexing, filtering, and CRUD operations."""

    def __init__(self, data_directory: str, file_name: str):
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / file_name
        self._lock = threading.RLock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        with self._lock:
            if not self.file_path.exists():
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)

    def read_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []

    def write_all(self, records: List[Dict[str, Any]]) -> None:
        with self._lock:
            temp_path = self.file_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, default=str)
            os.replace(temp_path, self.file_path)

    def find_by_id(self, record_id: str, id_field: str = "id") -> Optional[Dict[str, Any]]:
        records = self.read_all()
        for record in records:
            if str(record.get(id_field)) == str(record_id):
                return record
        return None

    def find_where(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        records = self.read_all()
        return [r for r in records if predicate(r)]

    def insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            records = self.read_all()
            records.append(record)
            self.write_all(records)
            return record

    def update(self, record_id: str, update_dict: Dict[str, Any], id_field: str = "id") -> Optional[Dict[str, Any]]:
        with self._lock:
            records = self.read_all()
            updated_record = None
            for idx, r in enumerate(records):
                if str(r.get(id_field)) == str(record_id):
                    records[idx].update(update_dict)
                    updated_record = records[idx]
                    break
            if updated_record:
                self.write_all(records)
            return updated_record

    def delete(self, record_id: str, id_field: str = "id") -> bool:
        with self._lock:
            records = self.read_all()
            initial_count = len(records)
            filtered_records = [r for r in records if str(r.get(id_field)) != str(record_id)]
            if len(filtered_records) < initial_count:
                self.write_all(filtered_records)
                return True
            return False

    def count(self) -> int:
        return len(self.read_all())

    def clear(self) -> None:
        with self._lock:
            self.write_all([])
