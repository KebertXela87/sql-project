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
-- Table structure for 3NF Types
--

DROP TABLE IF EXISTS types;
CREATE TABLE types (
    type_id int NOT NULL,
    type_name varchar(15) NOT NULL,
    PRIMARY KEY (type_id)
);

--
-- Data for types table
--

INSERT INTO types (type_id, type_name) VALUES
(1, 'Movie'),
(2, 'Novel'),
(3, 'YA Book'),
(4, 'Short Story'),
(5, 'Comic'),
(6, 'TV Show');

-- ------------------------------------------------------------

--
-- Table stucture for 1NF movies
--

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(40) NOT NULL,
    year varchar(15) NOT NULL,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

--
-- Table structure for 3NF Novels
--

DROP TABLE IF EXISTS novels;
CREATE TABLE novels (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(40) NOT NULL,
    year varchar(15) NOT NULL,
    author_id int,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

--
-- Table structure for 3NF YA Books
--

DROP TABLE IF EXISTS ya_books;
CREATE TABLE ya_books (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(40) NOT NULL,
    year varchar(15) NOT NULL,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

--
-- Table structure for 3NF Short Stories
--

DROP TABLE IF EXISTS short_stories;
CREATE TABLE short_stories (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(60) NOT NULL,
    year varchar(15) NOT NULL,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

--
-- Table structure for 3NF Comics
--

DROP TABLE IF EXISTS comics;
CREATE TABLE comics (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(40) NOT NULL,
    year varchar(15) NOT NULL,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

--
-- Table structure for 3NF TV Shows
--

DROP TABLE IF EXISTS tv_shows;
CREATE TABLE tv_shows (
    timeline_id int NOT NULL,
    type_id int NOT NULL REFERENCES types(type_id),
    title varchar(40) NOT NULL,
    year varchar(15) NOT NULL,
    released date NOT NULL,
    PRIMARY KEY (timeline_id)
);

-- ------------------------------------------------------------

--
-- Data for movies table
--

INSERT INTO movies (timeline_id, type_id, title, year, released) VALUES 
(47, 1, 'Episode IV: A New Hope', '0 ABY', 'May 25, 1977'),
(69, 1, 'Episode V: The Empire Strikes Back', '3 ABY', 'May 21, 1980'),
(71, 1, 'Episode VI: Return of the Jedi', '4 ABY', 'May 25, 1983'),
(1, 1, 'Episode I: The Phantom Menace', '32 BBY', 'May 19, 1999'),
(3, 1, 'Episode II: Attack of the Clones', '22 BBY', 'May 16, 2002'),
(17, 1, 'Episode III: Revenge of the Sith', '19 BBY', 'May 19, 2005'),
(93, 1, 'Episode VII: The Force Awakens', '34 ABY', 'December 18, 2015'),
(94, 1, 'Episode VIII', '34+ ABY', 'December 15, 2017'),
(95, 1, 'Episode IX', '34+ ABY', 'May 24, 2019'),
(46, 1, 'Rogue One', '1-0 BBY', 'December 16, 2016'),
(29, 1, 'Han Solo Anthology Film', '10 BBY', 'December 31, 2018'),
(96, 1, 'Boba Fett Anthology Film', '?', 'December 31, 2020');

-- ------------------------------------------------------------

--
-- Data for novels table
--

INSERT INTO novels (timeline_id, type_id, title, year, author_id, released) VALUES
(14, 2, 'Dark Disciple', '19 BBY', 1, 'July 7, 2015'),
(19, 2, 'Lords of the Sith', '14 BBY', 2, 'April 28, 2015'),
(22, 2, 'Tarkin', '14 BBY', 3, 'November 4, 2014'),
(24, 2, 'A New Dawn', '11 BBY', 4, 'September 2, 2014'),
(53, 2, 'Heir to the Jedi', '0 ABY', 5, 'March 3, 2015'),
(68, 2, 'Battlefront: Twilight Company', '3 ABY', 6, 'November 3, 2015'),
(76, 2, 'Aftermath', '4 ABY', 7, 'September 4, 2015'),
(77, 2, 'Aftermath: Life Debt', '4-5 ABY', 7, 'July 19, 2016'),
(78, 2, 'Aftermath: Empire''s End', '4-5 ABY', 7, 'January 1, 2017'),
(82, 2, 'Bloodline', '28 ABY', 8, 'May 3, 2016');

-- ------------------------------------------------------------

--
-- Data for ya_books table
--

INSERT INTO ya_books (timeline_id, type_id, title, year, released) VALUES
(30, 3, 'Edge of the Galaxy', '6 BBY', 'October 21, 2014'),
(34, 3, 'Ezra''s Gamble', '5 BBY', 'August 5, 2014'),
(37, 3, 'Rebel in the Ranks', '5 BBY', 'March 3, 2015'),
(39, 3, 'Imperial Justice', '4 BBY', 'July 7, 2015'),
(40, 3, 'The Secret Academy', '4 BBY', 'October 6, 2015'),
(49, 3, 'Smuggler''s Run', '0 ABY', 'September 4, 2015'),
(54, 3, 'The Weapon of a Jedi', '0 ABY', 'September 4, 2015'),
(70, 3, 'Moving Target', '3-4 ABY', 'September 4, 2015'),
(79, 3, 'Lost Stars', '0-5 ABY', 'September 4, 2015'),
(81, 3, 'Join the Resistance', '5 ABY', 'October 25, 2016'),
(91, 3, 'Before the Awakening', '33 ABY', 'December 18, 2015');

-- ------------------------------------------------------------

--
-- Data for short_stories table
--

INSERT INTO short_stories (timeline_id, type_id, title, year, released) VALUES
(13, 4, 'Kindred Spirits', '19 BBY', 'July 21, 2015'),
(20, 4, 'Orientation', '14 BBY', 'April 21, 2015'),
(21, 4, 'Mercy Mission', '14 BBY', 'October 6, 2015'),
(23, 4, 'Bottleneck', '14-11 BBY', 'October 6, 2015'),
(28, 4, 'End of History, The', '10 BBY', 'December 9, 2014'),
(42, 4, 'Rebel Bluff', '5-4 BBY', 'June 9, 2015'),
(50, 4, 'Last Call at the Zero Angle', '4 BBY', 'March 10, 2015'),
(51, 4, 'One Thousand Levels Down', '0 ABY', 'July 22, 2014'),
(67, 4, 'Inbrief', '0 ABY', 'November 10, 2015'),
(72, 4, 'Blade Squadron', '3 ABY', 'April 22, 2014'),
(73, 4, 'Blade Squadron: Zero Hour', '4 ABY', 'September 22, 2015'),
(74, 4, 'The Levers of Power', '4 ABY', 'October 6, 2015'),
(83, 4, 'The Perfect Weapon', '4 ABY', 'November 24, 2015'),
(84, 4, 'High Noon on Jakku', '34 ABY', 'November 30, 2015'),
(85, 4, 'All Creatures Great and Small', '34 ABY', 'November 30, 2015'),
(86, 4, 'Face of Evil, The', '34 ABY', 'November 30, 2015'),
(87, 4, 'The Crimson Corsair and the Lost Treasure of Count Dooku', '34 ABY', 'April 5, 2016'),
(88, 4, 'True Love', '34 ABY', 'April 5, 2016'),
(89, 4, 'A Recipe for Death', '34 ABY', 'December 22, 2015'),
(90, 4, 'Bait', '34 ABY', 'April 27, 2016');

-- ------------------------------------------------------------

--
-- Data for comics table
--

INSERT INTO comics (timeline_id, type_id, title, year, released) VALUES
(2, 5, 'Obi-Wan & Anakin', '22-19 BBY', 'January 1, 2016'),
(15, 5, 'Son of Dathomir', '19 BBY', 'May 21, 2014'),
(16, 5, 'First Blood', '19 BBY', 'October 28, 2015'),
(18, 5, 'The Last Padawan', '19 BBY', 'April 1, 2015'),
(25, 5, 'The Last of His Bree', '11 BBY', 'July 29, 2015'),
(26, 5, 'Ben Kenobi''s Journal #2', '10 BBY', 'January 20, 2016'),
(27, 5, 'Ben Kenobi''s Journal #3', '10 BBY', 'June 1, 2016'),
(41, 5, 'Haunt', '5-4 BBY', 'September 26, 2015'),
(48, 5, 'Princess Leia', '4 BBY', 'March 4, 2015'),
(52, 5, 'Chewbacca', '0 ABY', 'October 14, 2015'),
(55, 5, 'Skywalker Strikes', '0 ABY', 'January 14, 2015'),
(56, 5, 'Vader', '0 ABY', 'February 11, 2015'),
(57, 5, 'Showdown on the Smuggler''s Moon', '0 ABY', 'August 19, 2015'),
(58, 5, 'Darth Vader: Annual #1', '0 ABY', 'December 16, 2015'),
(59, 5, 'Shadows and Secrets', '0 ABY', 'July 1, 2015'),
(60, 5, 'Vader Down', '0-1 ABY', 'November 18, 2015'),
(61, 5, 'Star Wars: Annual #1', '0-1 ABY', 'December 9, 2015'),
(62, 5, 'The Shu-Torun War', '0-1 ABY', 'February 10, 2016'),
(63, 5, 'Rebel Jail', '0-1 ABY', 'February 17, 2016'),
(64, 5, 'End of Games', '0-1 ABY', 'May 11, 2016'),
(65, 5, 'Lando', '0-3 ABY', 'July 8, 2015'),
(66, 5, 'Han Solo', '0-3 ABY', 'June 1, 2016'),
(75, 5, 'Shattered Empire', '4 ABY', 'September 9, 2015'),
(80, 5, 'C-3PO #1', '4-34 ABY', 'April 13, 2016'),
(92, 5, 'Poe Dameron', '34 ABY', 'April 6, 2016');

-- ------------------------------------------------------------

--
-- Data for tv_shows table
--

INSERT INTO tv_shows (timeline_id, type_id, title, year, released) VALUES
(4, 6, 'Star Wars: The Clone Wars', '22 BBY', 'August 15, 2008'),
(5, 6, 'The Clone Wars: Season 1', '22-21 BBY', 'October 3, 2008'),
(6, 6, 'The Clone Wars: Season 2', '22-21 BBY', 'October 9, 2009'),
(7, 6, 'The Clone Wars: Season 3', '21-20 BBY', 'September 17, 2010'),
(8, 6, 'The Clone Wars: Season 4', '21-20 BBY', 'September 16, 2011'),
(9, 6, 'The Clone Wars: Season 5', '20 BBY', 'September 29, 2012'),
(10, 6, 'The Clone Wars: Season 6', '19 BBY', 'March 7, 2014'),
(11, 6, 'Crystal Crisis on Utapau', '19 BBY', 'September 25, 2014'),
(12, 6, 'The Bad Batch', '19 BBY', 'April 29, 2015'),
(31, 6, 'The Machine in the Ghost', '5 BBY', 'August 11, 2014'),
(32, 6, 'Art Attack', '5 BBY', 'August 18, 2014'),
(33, 6, 'Entanglement', '5 BBY', 'August 25, 2014'),
(35, 6, 'Property of Ezra Bridger', '5 BBY', 'September 1, 2014'),
(36, 6, 'Spark of Rebellion', '5 BBY', 'October 3, 2014'),
(38, 6, 'Rebels: Season 1', '5-4 BBY', 'October 13, 2014'),
(43, 6, 'The Siege of Lothal', '4 BBY', 'June 20, 2015'),
(44, 6, 'Rebels: Season 2', '4-3 BBY', 'October 14, 2015'),
(45, 6, 'Rebels: Season 3', '3 BBY', 'September 30, 2016');

-- ------------------------------------------------------------

--
-- GRANT PERMISSIONS
--
GRANT select, insert ON users TO jedimaster;
GRANT select, usage ON users_id_seq TO jedimaster;
GRANT select ON movies TO jedimaster;
GRANT select ON novels TO jedimaster;
GRANT select ON ya_books TO jedimaster;
GRANT select ON short_stories TO jedimaster;
GRANT select ON comics TO jedimaster;
GRANT select ON tv_shows TO jedimaster;
GRANT select ON types TO jedimaster;