INSERT INTO users (id, email, name, password, role) VALUES
    (
        'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        'admin@cabin-browser.com',
        'admin',
        '$2y$10$uDrhG8w591adqZWnU0kfRu2VeaKxvohnboEcCE.pErpCRmouEbyDa', -- password is admin
        'admin'
    ),
    (
        '4ccad0e9-f90f-4d0f-ba2f-47fb9265b8db',
        'kalle.kayttaja@email.com',
        'Kalle Kayttaja',
        '$2y$10$CPLGcF5nLdPpOyt9ocQ.K.PnH9p2iS4YGO8uUQGoPplC0VYXFlCEG', -- password is salasana
        'customer'
    ),
    (
        'e8002690-5578-49e7-ad8c-a16a667f5107',
        'olli.omistaja@email.com',
        'Olli Omistaja',
        '$2y$10$CPLGcF5nLdPpOyt9ocQ.K.PnH9p2iS4YGO8uUQGoPplC0VYXFlCEG', -- password is salasana
        'customer'
    );
