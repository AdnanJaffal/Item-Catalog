-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database
CREATE DATABASE tournament;

\c tournament;


-- Create PLAYERS table
-- Columns: ID (int), NAME (varchar), WINS (int), TOTAL (int), POINTS (int), Primary Key (ID)
CREATE TABLE PLAYERS(
  ID INT                NOT NULL,
  NAME VARCHAR(20)      NOT NULL,
  WINS INT              NOT NULL,
  TOTAL INT             NOT NULL,
  POINTS INT            NOT NULL,
  Primary Key (ID)
);

-- Create MATCHES table
-- Columns: ID (int), WINNER (varchar), LOSER (varchar), Primary Key (ID)
CREATE TABLE MATCHES(
  ID INT                NOT NULL,
  WINNER VARCHAR(20)    NOT NULL,
  LOSER VARCHAR(20)     NOT NULL,
  Primary Key (ID)
);


-- Create PLAYER_STANDINGS view
-- Columns: ID, NAME, WINS, TOTAL
-- Sorted by WINS
CREATE VIEW PLAYER_STANDINGS AS SELECT ID,NAME,WINS,TOTAL FROM PLAYERS ORDER BY WINS;