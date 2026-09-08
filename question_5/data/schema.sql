PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decription TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NULL,
    CONSTRAINT users_fk
        FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE user_claims (
    user_id INTEGER NOT NULL,
    claim_id INTEGER NOT NULL,
    CONSTRAINT user_claims_un
        UNIQUE (user_id, claim_id),
    CONSTRAINT user_claims_fk
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT user_claims_fk_1
        FOREIGN KEY (claim_id) REFERENCES claims(id)
);

-- Seed data for local development and tests.
INSERT INTO roles (description)
VALUES
    ('Administrator'),
    ('User'),
    ('Manager');