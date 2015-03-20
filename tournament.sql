-- Table definitions for the tournament project.
--
--
-- "players"
--
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT);
--
--
-- "matches"
--      Have a separate winner column to allow for ties (winner=None/Null)
--      Nice to have a timestamp for when match is recorded
--
CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	player_1 INT REFERENCES players (id),
	player_2 INT NULL REFERENCES players (id),
	winner INT NULL REFERENCES players (id),
	match_recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
--
--
--
--
-- ----------------
-- VIEWS BELOW HERE
-- ----------------
--
-- "player_matches"
--      Create a view to get the number of MATCHES for each player - rows with 0 if no matches
--
CREATE VIEW player_matches AS 
	SELECT p.id as player_id, count(m.id) as matches 
	FROM players as p 
		LEFT JOIN matches as m ON p.id = m.player_1 OR p.id = m.player_2
	GROUP BY p.id;
--
--
-- "player_wins"
--      Create a view to get the number of WINS for each player - rows with 0 if no wins
--
CREATE VIEW player_wins AS 
	SELECT p.id as player_id, count(m.id) as wins
	FROM players as p 
		LEFT JOIN matches as m ON p.id = m.winner
	GROUP BY p.id;
--
--
-- "player_ties"
--      Create a view to get the number of TIES for each player - rows with 0 if no ties
--
CREATE VIEW player_ties AS
    SELECT p.id as player_id, count(m.player_1)-count(m.winner) as ties
    FROM players as p
        LEFT JOIN matches as m on p.id=m.player_1 or p.id=m.player_2
    GROUP BY p.id;
--
--
-- "player_byes"
--      Create a view to get the number of BYES for each player - rows with 0 if no byes
--
CREATE VIEW player_byes AS
    SELECT p.id as player_id, count(m.player_1)-count(m.player_2) as byes
    FROM players as p
        LEFT JOIN matches as m on p.id=m.winner
    GROUP BY p.id;
--
--
-- "player_omw"
--      Create a view to get the number of OPPONENT MATCH WINS for each player - rows with 0 if no byes
--
CREATE VIEW player_omw AS
    SELECT p.id as player_id, sum(pw.wins) as omw
    FROM players as p
        LEFT JOIN player_wins as pw 
            ON pw.player_id IN 
                (SELECT DISTINCT player_1 AS opp FROM matches WHERE player_2=p.id 
                UNION ALL 
                SELECT DISTINCT player_2 AS opp FROM matches WHERE player_1=p.id)
    GROUP BY p.id;
	