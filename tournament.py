#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
#
# Extra Options:
#
# done - 1. Don't assume an even number of players. If there is an odd number of players, assign one player a bye (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.
# done - 2. Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.
# done - 3. When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
# 4. Support more than one tournament in the database, so matches do not have to be deleted between tournaments. This will require distinguishing between "a registered player" and "a player who has entered in tournament #123", so it will require changes to the database schema.
#

import time
import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE FROM matches""")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE FROM players""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) AS num FROM players""")
    result = cur.fetchall()
    return result[0][0]
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
    Args:
      name: the player's full name.
    """

    # so fresh and so clean clean
    name = bleach.clean(name)
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO players (name) VALUES (%s)""",(name,))
    conn.commit()
    conn.close()
    
    
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins, then ties, then OMW (opponent match win rate).

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id
        name: the player's full name (from registerPlayer)
        wins: the number of matches the player has won
        ties: the number of ties for the player
        matches: the number of matches the player has played
    """
        
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT p.id,p.name,pw.wins,pt.ties,pm.matches
                    FROM players as p 
                        JOIN player_wins as pw ON p.id = pw.player_id
                        JOIN player_ties as pt ON p.id = pt.player_id
                        JOIN player_matches as pm ON p.id = pm.player_id
                        JOIN player_omw as po ON p.id = po.player_id
                    ORDER BY pw.wins DESC, pt.ties DESC, po.omw DESC
                     """)
    rows  = cur.fetchall()
    standings = [(row[0],row[1],row[2],long(row[3]),row[4]) for row in rows]    
    conn.close()
    return standings

    
def reportMatch(player_1, player_2=None, winner=None):
    """Records the outcome of a single match between two players or a bye for player_1.

    Arguments:
      player_1:  the id number of the player 1
      player_2:  the id number of the player 2 - if None, then this is a bye (win) for player_1
      winner:    the id number of the player who won - if None, then the result was a tie
    """
    
    # If this is a bye (no player_2), then make player_1 the winner
    if player_2==None:
        winner = player_1
        
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO matches 
                   (player_1,player_2,winner)
                    VALUES (%s,%s,%s)
                 """,(player_1,player_2,winner))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    
    # We may need to remove a player receiving a bye, so create a new filtered list
    players_this_round = []
    
    # Get the next player to receive a bye (if applicable), and remove it from the list
    #   nextBye() will already return the id, so we just want to exclude it from the pairings.
    bye_id = nextBye()
    if bye_id:
        for(i,n,w,t,m) in standings:
            players_this_round.append((i,n,w,t,m))
    else:
        players_this_round = standings
    
    # Split up the list then put it back together so adjacent players get paired
    evens = players_this_round[::2]
    odds = players_this_round[1::2]
    pairs = zip(evens,odds)
    
    pairings = []
    for ((id1,name1,wins1,ties1,matches1),(id2,name2,wins2,ties2,matches2)) in pairs:
        pairings.append((id1,name1,id2,name2))
    return pairings


    
def nextBye():
    """If we have an odd number of players, return a player id that hasn't yet had a bye"""
    
    players = countPlayers()
    
    #if the player count is divisible by 2, then we don't need a bye
    if players%2==0:
        return False
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT player_id FROM player_byes ORDER BY byes ASC LIMIT 1""")
    result = cur.fetchall()
    conn.close()
    return result[0][0]

    
    
    
    
    

    
    
    
    