from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.team import Team

class TeamRepository:
    """Repository handling Team data persistence and default seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "teams.json")
        self._seed_default_teams()

    def _seed_default_teams(self) -> None:
        if self.store.count() == 0:
            defaults = [
                Team("Core Platform & DevOps", "Infrastructure and DevOps tooling", "admin", members=["admin", "devops"]),
                Team("FinTech Core Services", "Payment and financial processing", "devops", members=["devops", "developer"]),
                Team("Security & Identity", "Auth, IAM, and Security governance", "developer", members=["developer", "qa"])
            ]
            for t in defaults:
                self.store.insert(t.to_dict())

    def get_by_id(self, team_id: str) -> Optional[Team]:
        data = self.store.find_by_id(team_id)
        return Team.from_dict(data) if data else None

    def get_all(self) -> List[Team]:
        return [Team.from_dict(r) for r in self.store.read_all()]

    def save(self, team: Team) -> Team:
        existing = self.get_by_id(team.id)
        if existing:
            self.store.update(team.id, team.to_dict())
        else:
            self.store.insert(team.to_dict())
        return team
