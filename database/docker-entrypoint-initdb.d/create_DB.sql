CREATE DATABASE  log_bd_linux;
\connect  log_bd_linux

CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    second_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    token_hash TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE models (
    model_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    llm VARCHAR(255) NOT NULL,
    UNIQUE (user_id, llm)
);
CREATE TABLE chats (
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    session_id TEXT NOT NULL,
    llm VARCHAR(255) NOT NULL,
    unsafe_count BIGINT NOT NULL DEFAULT 0,
    last_bad_id BIGINT,
    checked BOOLEAN NOT NULL DEFAULT TRUE,
    misclassified BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (user_id, session_id)
);
CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    ip VARCHAR(255),
    session_id VARCHAR(255) NOT NULL,
    content TEXT,
    label VARCHAR(255),
    detected_by VARCHAR(255),
    role VARCHAR(255) NOT NULL,
    ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tokens BIGINT DEFAULT 0,
    costs DECIMAL (20,4)
);
CREATE TABLE api_keys (
    api_key_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    key_hash TEXT NOT NULL,
    key_value TEXT NOT NULL,
    key_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    last_used TIMESTAMPTZ,
    ts TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bot_users (
    tg_user_id BIGINT PRIMARY KEY,
    api_key TEXT,
    session_id TEXT
);
