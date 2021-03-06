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
    id               SERIAL         PRIMARY KEY,
    name             TEXT           NOT NULL,
    address          TEXT           NOT NULL UNIQUE,
    price            BIGINT         NOT NULL, -- Microcurrency
    description      TEXT,
    municipality_id  INTEGER        NOT NULL,
    owner_id         UUID           NOT NULL,

    FOREIGN KEY(municipality_id)         REFERENCES municipalities(id),
    FOREIGN KEY(owner_id)                REFERENCES users(id)
);

CREATE TABLE reviews (
    id          SERIAL      PRIMARY KEY,
    content     TEXT,
    rating      SMALLINT    NOT NULL,
    user_id     UUID        NOT NULL,
    cabin_id    INTEGER     NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(cabin_id) REFERENCES cabins(id) ON DELETE CASCADE
);

CREATE TABLE reservations (
    id              SERIAL      PRIMARY KEY,
    start_date      DATE        NOT NULL,
    end_date        DATE        NOT NULL,
    user_id         UUID        NOT NULL,
    cabin_id        INTEGER     NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(cabin_id) REFERENCES cabins(id) ON DELETE CASCADE
);

CREATE TABLE cabin_images(
    id          SERIAL  PRIMARY KEY,
    data        TEXT    NOT NULL,
    cabin_id    INTEGER NOT NULL,
    is_default  BOOLEAN NOT NULL,

    FOREIGN KEY(cabin_id) REFERENCES cabins(id) ON DELETE CASCADE
);

CREATE TABLE keywords(
    id          SERIAL PRIMARY KEY,
    keyword     TEXT     NOT NULL UNIQUE
);

CREATE TABLE cabins_keywords(
    keyword_id INTEGER NOT NULL,
    cabin_id   INTEGER NOT NULL,

    FOREIGN KEY(cabin_id) REFERENCES cabins(id) ON DELETE CASCADE,
    FOREIGN KEY(keyword_id) REFERENCES keywords(id)
);

CREATE UNIQUE INDEX on cabin_images (cabin_id) WHERE is_default;
