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

    #SQL query to clear MATCHES table
    QUERY = "DELETE FROM MATCHES;"

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Execute query
    c.execute(QUERY)

    #Close SQL connection
    conn.commit()
    conn.close()
    

def deletePlayers():
    """Remove all the player records from the database."""

    #SQL query to clear PLAYERS table
    QUERY = "DELETE FROM PLAYERS;"

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Execute query
    c.execute(QUERY)

    #Close SQL connection
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    #SQL query to count total players in PLAYERS table
    QUERY = "SELECT COUNT(ID) FROM PLAYERS;"

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Execute SQL query
    c.execute(QUERY)

    #Retreive results from query
    num = c.fetchone()

    #Close SQL connection
    conn.commit()
    conn.close()

    #Return results
    return num[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    #SQL query to insert new player in PLAYERS table
    QUERY = "INSERT INTO PLAYERS(NAME,WINS,TOTAL,POINTS) VALUES (%s, 0, 0, 0);"
    DATA = ("" + name + "",)

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Execute SQL query
    c.execute(QUERY, DATA)

    #Close SQL connection
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    #SQL query
    QUERY = "SELECT * FROM PLAYER_STANDINGS;"

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Retreive player data from PLAYER_STANDINGS view
    c.execute(QUERY)
    standings = c.fetchall()

    #Close SQL connection
    conn.commit()
    conn.close()

    #Return current standings
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    # Retreive name of winner and loser
    c.execute("SELECT NAME FROM PLAYERS WHERE ID = %s;", (winner,))
    winner_name = c.fetchone()
    c.execute("SELECT NAME FROM PLAYERS WHERE ID = %s;", (loser,))
    loser_name = c.fetchone()

    #Insert match into MATCHES table
    c.execute('INSERT INTO MATCHES(WINNER,WIN_ID,LOSER,LOSE_ID) VALUES(%s, %s,'
              ' %s, %s);', (str(winner_name[0]), winner, str(loser_name[0]),
                            loser))

    #Update winner with +1 point and winer + loser with +1 total matches
    c.execute("UPDATE PLAYERS SET WINS = WINS + 1, TOTAL = TOTAL + 1, POINTS ="
              " POINTS + 1 WHERE ID = %s AND NAME = %s;", (str(winner),
                                                        str(winner_name[0])))
    c.execute("UPDATE PLAYERS SET TOTAL = TOTAL + 1 WHERE ID = %s AND NAME = "
              "%s;", (str(loser), str(loser_name[0])))

    #Close SQL connection
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

    #Connect to SQL database
    conn = connect()
    c = conn.cursor()

    #Count number of players
    num = countPlayers()
    
    #Get current standings
    c.execute("SELECT ID,NAME FROM PLAYER_STANDINGS;")
    standings = c.fetchall()

    #Close sql connection
    conn.commit()
    conn.close()

    #Create tuple of pairings
    pairings = [(standings[x-1] + standings[x]) for x in range(1, num, 2)]

    #Return pairings
    return pairings

    


