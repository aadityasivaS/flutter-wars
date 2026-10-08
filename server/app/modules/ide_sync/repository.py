"""Database boundary for Module C credentials."""

from sqlalchemy import select
from sqlmodel import Session

from app.modules.ide_sync.model import TeamApiKey


class ApiKeyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, key: TeamApiKey) -> None:
        self.session.add(key)

    def get(self, key_id: str) -> TeamApiKey | None:
        return self.session.get(TeamApiKey, key_id)

    def active_for_team(self, team_id: str) -> list[TeamApiKey]:
        return list(
            self.session.exec(
                select(TeamApiKey).where(
                    TeamApiKey.team_id == team_id, TeamApiKey.status == "active"
                )
            )
        )
