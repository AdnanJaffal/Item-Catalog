#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    QUERY = "DELETE FROM MATCHES;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)
    conn.commit()
    conn.close()
    

def deletePlayers():
    """Remove all the player records from the database."""
    QUERY = "DELETE FROM PLAYERS;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    QUERY = "SELECT COUNT(ID) FROM PLAYERS;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)

    num = c.fetchone()
    
    conn.commit()
    conn.close()

    return num[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    QUERY = "INSERT INTO PLAYERS(NAME,WINS,TOTAL,POINTS) VALUES ('" + name + "', 0, 0, 0);"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    QUERY = "SELECT * FROM PLAYER_STANDINGS;"

    conn = connect()
    c = conn.cursor()
    c.execute(QUERY)
    standings = c.fetchall()
    conn.commit()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    QUERY_WIN = ("UPDATE PLAYERS SET WINS = WINS + 1, TOTAL = TOTAL + 1, POINTS = POINTS + 1 WHERE ID = (%i);", (winner))
    QUERY_LOSE = ("UPDATE PLAYERS SET TOTAL = TOTAL + 1 WHERE ID = (%i);", (loser))

    conn = connect()
    c = conn.cursor()

    # Retreive name of winner and loser
    c.execute(("SELECT NAME FROM PLAYERS WHERE ID = (?);", (winner)))
    winner_name = c.fetchone()
    c.execute("SELECT NAME FROM PLAYERS WHERE ID = (%i);", (loser))
    loser_name = c.fetchone()
    
    c.execute("INSERT INTO MATCHES VALUES('" + winner_name + "', '" + loser_name + "');")
    c.execute(QUERY_WIN)
    c.execute(QUERY_LOSE)
    conn.commit()
    conn.close()    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


