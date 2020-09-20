CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	email TEXT NOT NULL,
	password TEXT NOT NULL,
        bio TEXT NOT NULL,
        urole TEXT NOT NULL
);

CREATE TABLE admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        bio TEXT NOT NULL,
)
