from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.artifact import Artifact

class ArtifactRepository:
    """Repository handling Artifact registry persistence and default seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "artifacts.json")
        self._seed_default_artifacts()

    def _seed_default_artifacts(self) -> None:
        if self.store.count() == 0:
            defaults = [
                Artifact("devopsflow-core", "v1.0.0", "wheel", 4587520, "e3b0c44298fc1c149afbf4c8996fb924"),
                Artifact("payment-gateway-pkg", "v2.0.1", "tar", 12582912, "f2ca1bb6c7e907d06dafe4687e579fce"),
                Artifact("auth-subsystem-image", "v1.1.2", "container_image", 154828800, "9f86d081884c7d659a2feaa0c55ad015")
            ]
            for a in defaults:
                self.store.insert(a.to_dict())

    def get_by_id(self, artifact_id: str) -> Optional[Artifact]:
        data = self.store.find_by_id(artifact_id)
        return Artifact.from_dict(data) if data else None

    def get_all(self) -> List[Artifact]:
        return [Artifact.from_dict(r) for r in self.store.read_all()]

    def save(self, artifact: Artifact) -> Artifact:
        existing = self.get_by_id(artifact.id)
        if existing:
            self.store.update(artifact.id, artifact.to_dict())
        else:
            self.store.insert(artifact.to_dict())
        return artifact

    def delete(self, artifact_id: str) -> bool:
        return self.store.delete(artifact_id)
