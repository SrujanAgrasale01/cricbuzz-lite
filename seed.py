"""Create the schema and a compact demonstration dataset."""
from db import get_connection, initialize_database

def seed() -> None:
    initialize_database()
    with get_connection() as c:
        c.executescript("""
        DELETE FROM fielding_performances; DELETE FROM bowling_performances;
        DELETE FROM batting_performances; DELETE FROM innings; DELETE FROM match_teams;
        DELETE FROM matches; DELETE FROM series; DELETE FROM venues; DELETE FROM players; DELETE FROM teams;
        """)
        c.executemany("INSERT INTO teams(team_name,country) VALUES (?,?)", [
            ("India", "India"), ("Australia", "Australia"), ("England", "England"),
            ("South Africa", "South Africa"), ("New Zealand", "New Zealand"), ("Pakistan", "Pakistan")])
        c.executemany("INSERT INTO players(full_name,country,playing_role,batting_style,bowling_style) VALUES (?,?,?,?,?)", [
            ("Rohit Sharma","India","Batsman","Right-hand","Right-arm off break"),
            ("Virat Kohli","India","Batsman","Right-hand","Right-arm medium"),
            ("Jasprit Bumrah","India","Bowler","Right-hand","Right-arm fast"),
            ("Ben Stokes","England","All-rounder","Left-hand","Right-arm fast-medium"),
            ("Pat Cummins","Australia","Bowler","Right-hand","Right-arm fast"),
            ("Kane Williamson","New Zealand","Batsman","Right-hand","Right-arm off break"),
            ("Quinton de Kock","South Africa","Wicket-keeper","Left-hand","Right-arm medium"),
            ("Babar Azam","Pakistan","Batsman","Right-hand","Right-arm off break")])
        c.executemany("INSERT INTO venues(venue_name,city,country,capacity) VALUES (?,?,?,?)", [
            ("Wankhede Stadium","Mumbai","India",33000), ("Melbourne Cricket Ground","Melbourne","Australia",100024),
            ("Lord's","London","England",30000), ("Eden Gardens","Kolkata","India",68000)])
        c.executemany("INSERT INTO series(series_name,host_country,match_type,start_date,total_matches) VALUES (?,?,?,?,?)", [
            ("2024 Border-Gavaskar Test Series","Australia","Test","2024-11-22",5),
            ("2024 Champions ODI Tour","India","ODI","2024-06-01",8),
            ("2025 International T20 Cup","South Africa","T20I","2025-02-01",12)])
        c.executemany("""INSERT INTO matches(series_id,match_description,format,match_date,venue_id,status,
                       toss_winner_id,toss_decision,winning_team_id,victory_margin,victory_type)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?)""", [
            (1,"India vs Australia, 1st Test","Test","2024-11-22",2,"Completed",1,"bat",1,295,"runs"),
            (2,"India vs England, ODI","ODI","2024-06-10",4,"Completed",3,"bowl",1,6,"wickets"),
            (3,"India vs South Africa, T20I","T20I","2025-02-05",1,"Completed",1,"bowl",4,12,"runs"),
            (2,"Australia vs New Zealand, ODI","ODI","2025-01-20",2,"Completed",2,"bat",2,44,"runs"),
            (3,"Pakistan vs England, T20I","T20I","2025-02-10",3,"Completed",3,"bowl",6,3,"wickets")])
        c.executemany("INSERT INTO match_teams(match_id,team_id,is_home,is_winner) VALUES (?,?,?,?)", [
            (1,1,1,1),(1,2,0,0),(2,1,1,1),(2,3,0,0),(3,1,1,0),(3,4,0,1),
            (4,2,1,1),(4,5,0,0),(5,6,1,1),(5,3,0,0)])
        c.executemany("INSERT INTO innings(match_id,innings_number,batting_team_id,bowling_team_id,total_runs,total_wickets) VALUES (?,?,?,?,?,?)", [
            (1,1,1,2,450,10),(1,2,2,1,155,10),(2,1,1,3,320,7),(2,2,3,1,314,10),
            (3,1,4,1,180,6),(3,2,1,4,168,10),(4,1,2,5,300,8),(4,2,5,2,256,10),
            (5,1,6,3,175,7),(5,2,3,6,172,10)])
        c.executemany("""INSERT INTO batting_performances(innings_id,player_id,batting_position,runs,balls,fours,sixes,not_out)
                       VALUES (?,?,?,?,?,?,?,?)""", [
            (1,1,1,210,300,20,3,0),(1,2,2,125,180,12,1,0),(1,4,3,65,90,7,0,0),
            (2,5,1,80,150,8,0,0),(2,6,2,42,100,4,0,0),(3,1,1,145,130,14,5,1),
            (3,2,2,90,85,9,2,0),(4,3,1,110,105,10,3,0),(4,7,2,95,98,8,1,0),
            (5,4,1,75,50,6,3,0),(5,1,2,60,42,5,2,0),(6,2,1,88,70,7,1,0),
            (6,1,2,55,45,4,2,0),(7,5,1,130,140,11,2,0),(7,6,2,70,90,5,1,0),
            (8,7,1,120,110,12,3,0),(8,5,2,66,65,6,1,0),(9,8,1,105,70,9,4,0),
            (9,4,2,50,38,4,2,0),(10,4,1,98,75,8,3,0),(10,8,2,35,30,3,1,0)])
        c.executemany("""INSERT INTO bowling_performances(innings_id,player_id,overs,runs_conceded,wickets,maidens)
                       VALUES (?,?,?,?,?,?)""", [
            (1,5,35,140,4,3),(1,3,32,120,3,4),(2,3,28,90,5,2),(2,5,30,110,2,1),
            (3,5,10,70,2,0),(3,4,8,55,1,0),(4,3,10,60,3,0),(4,5,10,75,2,0),
            (5,3,4,35,2,0),(5,5,4,42,1,0),(6,3,4,40,3,0),(6,5,4,45,2,0),
            (7,3,10,80,2,0),(7,5,10,75,3,0),(8,3,10,90,1,0),(8,5,10,65,4,0),
            (9,4,4,38,2,0),(9,3,4,44,1,0),(10,4,4,40,3,0),(10,3,4,48,2,0)])
        c.executemany("INSERT INTO fielding_performances(innings_id,player_id,catches,stumpings,run_outs) VALUES (?,?,?,?,?)", [
            (1,3,1,0,0),(2,1,2,0,0),(3,2,1,0,0),(4,7,2,1,0),(5,1,1,0,0),(6,2,2,0,1),
            (7,6,1,0,0),(8,7,2,1,0),(9,4,1,0,0),(10,8,1,0,0)])

if __name__ == "__main__":
    seed()
    print("Database initialized and seeded.")
