-- Module C schema. Apply through the deployment migration runner before
-- enabling the API-key endpoints against PostgreSQL.
CREATE TABLE team_api_key (
    key_id VARCHAR(32) PRIMARY KEY,
    team_id VARCHAR(128) NOT NULL,
    secret_hash VARCHAR(128) NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL,
    last_used_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE INDEX ix_team_api_key_team_id ON team_api_key (team_id);
CREATE INDEX ix_team_api_key_status ON team_api_key (status);
