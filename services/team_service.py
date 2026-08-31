from typing import Tuple, Optional, List, Dict, Any
from repositories.team_repo import TeamRepository
from models.team import Team
from core.events import EventBus

class TeamService:
    """Team management service."""

    def __init__(self, repository: TeamRepository):
        self.repo = repository

    def create_team(self, name: str, description: str, lead: str) -> Tuple[bool, Optional[Team], str]:
        if not name:
            return False, None, "Team name is required."

        t = Team(name=name.strip(), description=description.strip(), lead=lead)
        saved = self.repo.save(t)
        EventBus.publish("team_created", team_id=saved.id, name=saved.name)
        return True, saved, "Team created successfully."

    def add_member(self, team_id: str, username: str) -> Tuple[bool, str]:
        t = self.repo.get_by_id(team_id)
        if not t:
            return False, "Team not found."

        if username in t.members:
            return False, "User is already a member of this team."

        t.members.append(username)
        self.repo.save(t)
        return True, f"User {username} added to team {t.name}."
