CREATE DATABASE circlespace;
USE circlespace;

CREATE TABLE circle (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(12) NOT NULL,
    permalink CHAR(36) NOT NULL UNIQUE DEFAULT (UUID())
);

CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    circle_id INTEGER NOT NULL REFERENCES circle(id),
    name VARCHAR(12) NOT NULL
);
CREATE INDEX people_circle_id ON people (circle_id);

CREATE TABLE the_cfg (
    cfg_key VARCHAR(32) PRIMARY KEY,
    cfg_value VARCHAR(255)
);

INSERT INTO the_cfg (cfg_key, cfg_value) VALUES ("flag", "DUCTF{n0T_squar3spaCe_7o0N2kf1}");
