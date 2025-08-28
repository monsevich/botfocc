-- Sample SQL for dialog tables; canonical schema is managed by Django migrations.
CREATE TABLE IF NOT EXISTS dialog_session (
    id SERIAL PRIMARY KEY,
    external_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dialog_message (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES dialog_session(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
