PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS teams (
 team_id INTEGER PRIMARY KEY AUTOINCREMENT, team_name TEXT NOT NULL UNIQUE, country TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS players (
 player_id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, country TEXT NOT NULL,
 playing_role TEXT NOT NULL CHECK (playing_role IN ('Batsman','Bowler','All-rounder','Wicket-keeper')),
 batting_style TEXT, bowling_style TEXT);
CREATE TABLE IF NOT EXISTS venues (
 venue_id INTEGER PRIMARY KEY AUTOINCREMENT, venue_name TEXT NOT NULL, city TEXT NOT NULL,
 country TEXT NOT NULL, capacity INTEGER CHECK (capacity >= 0));
CREATE TABLE IF NOT EXISTS series (
 series_id INTEGER PRIMARY KEY AUTOINCREMENT, series_name TEXT NOT NULL, host_country TEXT NOT NULL,
 match_type TEXT NOT NULL, start_date TEXT NOT NULL, total_matches INTEGER NOT NULL CHECK(total_matches >= 0));
CREATE TABLE IF NOT EXISTS matches (
 match_id INTEGER PRIMARY KEY AUTOINCREMENT, series_id INTEGER REFERENCES series(series_id),
 match_description TEXT NOT NULL, format TEXT NOT NULL CHECK(format IN ('Test','ODI','T20I')),
 match_date TEXT NOT NULL, venue_id INTEGER REFERENCES venues(venue_id), status TEXT NOT NULL,
 toss_winner_id INTEGER REFERENCES teams(team_id), toss_decision TEXT CHECK(toss_decision IN ('bat','bowl')),
 winning_team_id INTEGER REFERENCES teams(team_id), victory_margin INTEGER, victory_type TEXT CHECK(victory_type IN ('runs','wickets')));
CREATE TABLE IF NOT EXISTS match_teams (
 match_id INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE, team_id INTEGER NOT NULL REFERENCES teams(team_id),
 is_home INTEGER NOT NULL DEFAULT 0 CHECK(is_home IN (0,1)), is_winner INTEGER NOT NULL DEFAULT 0 CHECK(is_winner IN (0,1)),
 PRIMARY KEY(match_id,team_id));
CREATE TABLE IF NOT EXISTS innings (
 innings_id INTEGER PRIMARY KEY AUTOINCREMENT, match_id INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
 innings_number INTEGER NOT NULL, batting_team_id INTEGER NOT NULL REFERENCES teams(team_id),
 bowling_team_id INTEGER NOT NULL REFERENCES teams(team_id), total_runs INTEGER DEFAULT 0, total_wickets INTEGER DEFAULT 0,
 UNIQUE(match_id,innings_number));
CREATE TABLE IF NOT EXISTS batting_performances (
 batting_id INTEGER PRIMARY KEY AUTOINCREMENT, innings_id INTEGER NOT NULL REFERENCES innings(innings_id) ON DELETE CASCADE,
 player_id INTEGER NOT NULL REFERENCES players(player_id), batting_position INTEGER NOT NULL, runs INTEGER NOT NULL CHECK(runs >= 0),
 balls INTEGER NOT NULL CHECK(balls >= 0), fours INTEGER DEFAULT 0, sixes INTEGER DEFAULT 0, not_out INTEGER DEFAULT 0 CHECK(not_out IN (0,1)));
CREATE TABLE IF NOT EXISTS bowling_performances (
 bowling_id INTEGER PRIMARY KEY AUTOINCREMENT, innings_id INTEGER NOT NULL REFERENCES innings(innings_id) ON DELETE CASCADE,
 player_id INTEGER NOT NULL REFERENCES players(player_id), overs REAL NOT NULL CHECK(overs >= 0), runs_conceded INTEGER DEFAULT 0,
 wickets INTEGER DEFAULT 0, maidens INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS fielding_performances (
 fielding_id INTEGER PRIMARY KEY AUTOINCREMENT, innings_id INTEGER NOT NULL REFERENCES innings(innings_id) ON DELETE CASCADE,
 player_id INTEGER NOT NULL REFERENCES players(player_id), catches INTEGER DEFAULT 0, stumpings INTEGER DEFAULT 0, run_outs INTEGER DEFAULT 0);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(format);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_performances(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_performances(player_id);
