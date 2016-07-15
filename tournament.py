
import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    database_name = "tournament"
    DB = psycopg2.connect("dbname={}".format(database_name))
    cursor = DB.cursor()
    return DB, cursor

def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute('''UPDATE matches 
                    SET matchnum = 0, wins = 0, losses = 0, draws = 0''')
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute('''TRUNCATE matches, players''')
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute('''SELECT count(playerid) AS num FROM players''')
    count = cursor.fetchone()[0] 
    DB.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).

    Selects player's playerid from players after adding a name, 
    then inserts playerid into matches.
    """
    DB, cursor = connect()
    insquery = '''INSERT INTO players (playername) VALUES (%s)'''
    value = (name,)
    cursor.execute(insquery, value)
    DB.commit()
    selquery = '''SELECT playerid FROM players 
                    WHERE playername = (%s)'''
    cursor.execute(selquery, value)
    ids = cursor.fetchall()[0][0]
    cursor.execute('''INSERT INTO matches VALUES (%s, %s, %s, %s, %s)''', (ids, 0, 0, 0, 0))
    # inserts playerid into matches when new player is registered
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, draws, matches):
        playerid: the player's unique playerid (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, cursor = connect()
    query = '''SELECT players.playerid, players.playername, matches.wins, 
                                matches.draws, matches.matchnum 
                    FROM players, matches 
                    WHERE players.playerid = matches.playerid 
                    ORDER BY wins desc, draws desc'''
    cursor.execute(query)
    standings = cursor.fetchall()
    DB.close()
    return standings

def reportMatch(winner, loser, draw1, draw2):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the playerid number of the player who won
      loser:  the playerid number of the player who lost
      draw1, draw2:  the playerid numbers of the players who drew
      'None' should go in winner and loser if the match drew, 
      or in draw1 and draw2 otherwise 
    """
    DB, cursor = connect()
    cursor.execute('''UPDATE matches SET matchnum = matchnum+1, wins = wins+1
                    WHERE playerid = (%s)''', (winner,))
    cursor.execute('''UPDATE matches SET matchnum = matchnum+1, losses = losses+1 
                    WHERE playerid = (%s)''', (loser,))
    if draw1 and draw2 != None:
        cursor.execute('''UPDATE matches SET matchnum = matchnum+1, draws = draws+1
                        WHERE playerid = (%s) or playerid = (%s)''', (draw1, draw2))
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        playerid1: the first player's unique id
        name1: the first player's name
        playerid2: the second player's unique id
        name2: the second player's name
    """
    DB, cursor = connect()
    cursor.execute('''CREATE VIEW allplayers as 
                    SELECT players.playerid, players.playername, matches.wins, 
                            matches.draws, matches.matchnum 
                    FROM players, matches 
                    WHERE players.playerid = matches.playerid''')
    cursor.execute('''SELECT * 
                    FROM allplayers''')
    all_players = cursor.fetchall()
    numplayers = len(all_players)
    if numplayers % 2 == 1:
        playerBye(numplayers, all_players)
        numplayers -= 1
    cursor.execute('''SELECT * 
                    FROM allplayers 
                    ORDER BY matchnum, wins desc, draws desc''')
    p = 0
    pairings = []
    while numplayers > p:
        pair = cursor.fetchmany(size = 2)
        pairings.append((pair[0][0], pair[0][1], pair[1][0], pair[1][1])) 
        p += 2 # advance 2 players at a time
    DB.close()
    return pairings

def playerBye(numplayers, all_players):
    DB, cursor = connect()
    byeid = all_players[random.randint(0, (numplayers - 1))][0] # single random playerid for bye
    query = '''UPDATE matches SET matchnum = matchnum+1, wins = wins+1 
                    WHERE playerid = (%s)'''
    cursor.execute(query, (byeid,))
    DB.commit()
    DB.close()