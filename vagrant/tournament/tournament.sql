-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database if it exists already
DROP DATABASE IF EXISTS tournament;


-- Create database
CREATE DATABASE tournament;

\c tournament;


-- Create PLAYERS table
-- Columns: ID (int), NAME (varchar), Primary Key (ID)
CREATE TABLE PLAYERS(
  P_ID SERIAL             NOT NULL,
  NAME VARCHAR(20)      NOT NULL,
  Primary Key (P_ID)
);

-- Create MATCHES table
-- Columns: ID (int), WIN_ID (int), LOSE_ID (int), Primary Key (ID), Foreign Key (WIN_ID, LOSE_ID)
CREATE TABLE MATCHES(
  M_ID SERIAL             NOT NULL,
  WIN_ID INT		NOT NULL,
  LOSE_ID INT		NOT NULL,
  Primary Key (M_ID),
  Foreign Key (WIN_ID) References PLAYERS(P_ID),
  Foreign Key (LOSE_ID) References PLAYERS(P_ID)
);


-- Create PLAYER_STANDINGS view
-- Columns: ID, NAME, WINS, TOTAL
-- Sorted by WINS
CREATE VIEW PLAYER_STANDINGS AS SELECT P_ID,NAME,(SELECT COUNT(*) FROM MATCHES WHERE MATCHES.WIN_ID = PLAYERS.P_ID) AS WINS, (SELECT COUNT(*) FROM MATCHES WHERE MATCHES.WIN_ID = PLAYERS.P_ID OR MATCHES.LOSE_ID = PLAYERS.P_ID) AS TOTAL FROM PLAYERS ORDER BY WINS DESC;