from uuid import uuid4

from sqlmodel import Session, SQLModel

from app.core.db import get_engine
from app.modules.authentication.jwt import create_access_token
from app.modules.authentication.model import Team, TeamMembership, UserIdentity


def _seed_team_a() -> tuple[int, int, str]:
    suffix = uuid4().hex
    subject = f"google-user-{suffix}"
    SQLModel.metadata.create_all(get_engine())
    with Session(get_engine()) as session:
        team = Team(name=f"Team A {suffix}")
        user = UserIdentity(google_subject=subject, email="a@example.test")
        session.add(team)
        session.add(user)
        session.commit()
        session.refresh(team)
        session.refresh(user)
        assert team.id is not None and user.id is not None
        session.add(TeamMembership(user_identity_id=user.id, team_id=team.id, role="participant"))
        session.commit()
        return user.id, team.id, subject


def test_google_login_and_me_resolve_current_membership(app, client):
    user_id, team_id, subject = _seed_team_a()
    app.state.google_token_verifier = lambda credential: (
        {"google_subject": subject, "email": "a@example.test"}
        if credential == "valid-google-token"
        else None
    )

    login = client.post("/auth/google", json={"credential": "valid-google-token"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json() == {
        "user_id": str(user_id),
        "email": "a@example.test",
        "team_id": str(team_id),
        "role": "participant",
        "auth_type": "JWT",
    }


def test_invalid_or_unregistered_google_identity_is_rejected(app, client):
    SQLModel.metadata.create_all(get_engine())
    app.state.google_token_verifier = lambda credential: None
    invalid = client.post("/auth/google", json={"credential": "bad-token"})
    assert invalid.status_code == 401
    assert invalid.json()["code"] == "INVALID_GOOGLE_CREDENTIAL"

    app.state.google_token_verifier = lambda credential: {
        "google_subject": "unregistered", "email": "unknown@example.test"
    }
    unregistered = client.post("/auth/google", json={"credential": "valid-but-unknown"})
    assert unregistered.status_code == 403
    assert unregistered.json()["code"] == "ACCOUNT_NOT_ALLOWED"


def test_jwt_team_and_role_claims_cannot_override_database_membership(app, client):
    user_id, team_a_id, _ = _seed_team_a()
    with Session(get_engine()) as session:
        team_b = Team(name=f"Team B {uuid4().hex}")
        session.add(team_b)
        session.commit()
        session.refresh(team_b)
        assert team_b.id is not None

    forged_team_token = create_access_token(
        user_id=str(user_id),
        email="a@example.test",
        team_id=str(team_b.id),
        role="organizer",
        settings=app.state.settings,
    )
    denied = client.get("/auth/me", headers={"Authorization": f"Bearer {forged_team_token}"})
    assert denied.status_code == 403
    assert denied.json()["code"] == "TEAM_ACCESS_DENIED"

    valid_token = create_access_token(
        user_id=str(user_id),
        email="a@example.test",
        team_id=str(team_a_id),
        role="organizer",
        settings=app.state.settings,
    )
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {valid_token}"})
    assert me.status_code == 200
    assert me.json()["role"] == "participant"
