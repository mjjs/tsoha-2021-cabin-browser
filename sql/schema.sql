CREATE TABLE users (
    id          UUID PRIMARY KEY,
    email       TEXT NOT NULL,
    name        TEXT NOT NULL,
    password    TEXT NOT NULL,
    role        TEXT NOT NULL
);

CREATE TABLE municipalities (
    id      SERIAL  PRIMARY KEY,
    name    TEXT    NOT NULL
);

CREATE TABLE cabins (
    id              SERIAL  PRIMARY KEY,
    address         TEXT    NOT NULL UNIQUE,
    municipality_id INTEGER NOT NULL,
    price           MONEY   NOT NULL,
    description     TEXT,

    FOREIGN KEY(municipality_id) REFERENCES municipalities(id)
);

CREATE TABLE reviews (
    id          SERIAL      PRIMARY KEY,
    content     TEXT,
    rating      SMALLINT    NOT NULL,
    user_id     UUID        NOT NULL,
    cabin_id    INTEGER     NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(cabin_id) REFERENCES cabins(id)
);

CREATE TABLE reservations (
    id              SERIAL      PRIMARY KEY,
    reserve_start   DATE        NOT NULL,
    reserve_end     DATE        NOT NULL,
    user_id         UUID        NOT NULL,
    cabin_id        INTEGER     NOT NULL UNIQUE,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(cabin_id) REFERENCES cabins(id)
);

CREATE TABLE cabin_images(
    id          SERIAL  PRIMARY KEY,
    filename    TEXT    NOT NULL,
    bytes       BYTEA   NOT NULL,
    cabin_id    INTEGER NOT NULL,

    FOREIGN KEY(cabin_id) REFERENCES cabins(id)
);
