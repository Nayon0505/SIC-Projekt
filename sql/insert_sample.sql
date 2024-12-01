BEGIN TRANSACTION;
DELETE from sqlite_sequence;
INSERT INTO user_data (email, password) VALUES ("nayon@gmail.com", "12345");

COMMIT;