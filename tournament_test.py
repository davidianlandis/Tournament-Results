#!/usr/bin/env python
#
# Test cases for tournamentec.py

from tournament import *
import math

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, wins1, ties1, matches1), (id2, name2, wins2, ties2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or ties1 != 0 or ties2 != 0:
        raise ValueError(
            "Newly registered players should have no matches, wins, or ties.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Timmy")
    registerPlayer("Jimmy")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    reportMatch(id5, id6)
    standings = playerStandings()
    for (i, n, w, t, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        elif i in (id5, id6) and t != 1:
            raise ValueError("Each match tie should have exactly one tie per player. %s(%i) = %i" % (n,i,t))
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Timmy")
    registerPlayer("Jimmy")
    registerPlayer("Stan")
    registerPlayer("Kyle")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    standings = playerStandings()
    pairings = swissPairings()
    
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return four pairs.")

    (pid1,pname1,pid2,pname2) = pairings[0]
    if set([pid1,pid2]) != set([id1,id3]):
        raise ValueError("Players with one win should be paired.")
        
    (pid1,pname1,pid2,pname2) = pairings[1]
    if set([pid1,pid2]) != set([id6,id8]) and set([pid1,pid2]) != set([id6,id8]):
        raise ValueError("Players with one tie should be paired.")
    (pid1,pname1,pid2,pname2) = pairings[2]
    if set([pid1,pid2]) != set([id5,id7]) and set([pid1,pid2]) != set([id5,id8]):
        raise ValueError("Players with one tie should be paired.")

    (pid1,pname1,pid2,pname2) = pairings[3]
    if set([pid1,pid2]) != set([id2,id4]):
        raise ValueError("Players with one loss should be paired.")
    
            
    print "8. After one match, players with one win are paired."


    
def testNextBye():
    deleteMatches()
    deletePlayers()

    registerPlayer("Joe")
    registerPlayer("Brad")
    registerPlayer("Sue")
    registerPlayer("Kelly")
    bye_id = nextBye()
    if bye_id:
        raise ValueError("There should NOT be a bye for an even number of players.")
    
    registerPlayer("Joe")
    registerPlayer("Brad")
    registerPlayer("Sue")
    registerPlayer("Kelly")
    registerPlayer("Bob")
    
    bye_id = nextBye()
    if not bye_id:
        raise ValueError("There SHOULD be a bye for an odd number of players.")
 
    print "9. Byes are only assigned for odd number of players."

    
def testByesInRounds():
    """
	Go through as many rounds as are required for the number of players.
        Make sure no one gets more than one bye
	"""
    deleteMatches()
    deletePlayers()
    
    registerPlayer("Joe")
    registerPlayer("Brad")
    registerPlayer("Sue")
    registerPlayer("Kelly")
    registerPlayer("Bob")
    
    rounds = int(math.floor(math.log(5,2)))
    byes = []
    
    for r in range(1,rounds+1):
        
        bye_id = nextBye()
        
        pairs = swissPairings()
        
        for (id1, name1, id2, name2) in pairs:
            reportMatch(id1,id2,id1) #luck of being player1
        
        if bye_id in byes:
            raise ValueError("No player should receive more than one bye.")
            
        if bye_id:
            reportMatch(bye_id)
            byes.append(bye_id)
    
    print "10. Players don't receive more than one bye."
    
 



    
    
if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testNextBye()
    testByesInRounds()
    print "Success!  All tests pass!"


