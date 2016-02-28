DROP DATABASE IF EXISTS thearchives;
CREATE DATABASE thearchives;
\c thearchives;
-- ------------------------------------------------------------

--
-- Create role
--

CREATE ROLE jedimaster LOGIN PASSWORD '41PubBNmfQhmfCNy';

-- ------------------------------------------------------------

--
-- Table structure for users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (id)
);

-- ------------------------------------------------------------

--
-- Table stucture for 1NF movies
--

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    movie_id int NOT NULL,
    title varchar(40) NOT NULL,
    released date NOT NULL,
    bby_aby_year varchar(15) NOT NULL,
    running_time varchar(15),
    PRIMARY KEY (movie_id)
);

--
-- Data for movies table
--

INSERT INTO movies (movie_id, title, released, bby_aby_year, running_time) VALUES 
(1, 'Episode IV: A New Hope', '1977-05-25', '0 BBY/ABY', '121 minutes'),
(2, 'Episode V: The Empire Strikes Back', '1980-05-21', '3 ABY', '124 minutes'),
(3, 'Episode VI: Return of the Jedi', '1983-05-25', '4 ABY', '131 minutes'),
(4, 'Episode I: The Phantom Menace', '1999-05-19', '32 BBY', '133 minutes'),
(5, 'Episode II: Attack of the Clones', '2002-05-16', '22 BBY', '142 minutes'),
(6, 'Episode III: Revenge of the Sith', '2005-05-19', '19 BBY', '140 minutes'),
(7, 'Episode VII: The Force Awakens', '2015-12-18', '34 ABY', '135 minutes'),
(8, 'Episode VIII', '2017-12-15', '34+ ABY', ''),
(9, 'Episode IX', '2019-05-24', '34+ ABY', ''),
(10, 'Rogue One', '2016-12-16', '1-0 BBY', ''),
(11, 'Han Solo Anthology Film', '2018-12-31', '10 BBY', ''),
(12, 'Boba Fett Anthology Film', '2020-12-31', '?', ''),
(13, 'The Clone Wars', '2008-08-15', '22 BBY', '98 minutes');

-- ------------------------------------------------------------

--
-- GRANT PERMISSIONS
--
GRANT select, insert ON users TO jedimaster;
GRANT select, usage ON users_id_seq TO jedimaster;
GRANT select ON movies TO jedimaster;