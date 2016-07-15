--To create and connect to the tournament database, type the
--following in your psql console:
--
--DROP DATABASE IF EXISTS tournament;
--CREATE DATABASE tournament;
--\c tournament
--
--Then, to create the following tables, you can either copy/paste
--the below commands into the psql console, or execute this file:
--
--\i tournament.sql
--
--If you need to drop the tables (maybe to make a correction),
--use this command:
--
--DROP TABLE <name>;
--
--You will then need to run this file again to create the tables.

CREATE TABLE players ( 
	playername TEXT, 
	playerid SERIAL PRIMARY KEY);

CREATE TABLE matches ( 
	playerid INTEGER REFERENCES players(playerid),
	matchnum INTEGER,
	wins INTEGER,
	losses INTEGER,
	draws INTEGER);
