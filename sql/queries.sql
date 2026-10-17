-- Q1: Indian players
SELECT full_name, playing_role, batting_style, bowling_style FROM players WHERE country = 'India' ORDER BY full_name;
-- Q2: Matches in last 30 days relative to 2025-02-15 demo date
SELECT m.match_description, t1.team_name team_1, t2.team_name team_2, v.venue_name, v.city, m.match_date
FROM matches m JOIN venues v ON v.venue_id=m.venue_id JOIN match_teams mt1 ON mt1.match_id=m.match_id AND mt1.is_home=1
JOIN teams t1 ON t1.team_id=mt1.team_id JOIN match_teams mt2 ON mt2.match_id=m.match_id AND mt2.is_home=0 JOIN teams t2 ON t2.team_id=mt2.team_id
WHERE m.match_date >= date('2025-02-15','-30 day') ORDER BY m.match_date DESC;
-- Q3: Top ODI run scorers
SELECT p.full_name, SUM(bp.runs) total_runs, ROUND(AVG(CASE WHEN bp.not_out=0 THEN bp.runs END),2) batting_average,
SUM(CASE WHEN bp.runs>=100 THEN 1 ELSE 0 END) centuries FROM players p JOIN batting_performances bp ON bp.player_id=p.player_id
JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id WHERE m.format='ODI' GROUP BY p.player_id ORDER BY total_runs DESC LIMIT 10;
-- Q4: Large venues
SELECT venue_name, city, country, capacity FROM venues WHERE capacity > 50000 ORDER BY capacity DESC;
-- Q5: Wins by team
SELECT t.team_name, COUNT(m.match_id) total_wins FROM teams t LEFT JOIN matches m ON m.winning_team_id=t.team_id GROUP BY t.team_id ORDER BY total_wins DESC;
-- Q6: Player count by role
SELECT playing_role, COUNT(*) player_count FROM players GROUP BY playing_role ORDER BY player_count DESC;
-- Q7: Highest individual score by format
SELECT m.format, MAX(bp.runs) highest_score FROM batting_performances bp JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY m.format;
-- Q8: Series started in 2024
SELECT series_name, host_country, match_type, start_date, total_matches FROM series WHERE strftime('%Y',start_date)='2024' ORDER BY start_date;
-- Q9: All-rounders over career thresholds
SELECT p.full_name, m.format, SUM(bp.runs) total_runs, COALESCE(SUM(bw.wickets),0) total_wickets FROM players p
JOIN batting_performances bp ON bp.player_id=p.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id
LEFT JOIN bowling_performances bw ON bw.player_id=p.player_id AND bw.innings_id=i.innings_id WHERE p.playing_role='All-rounder'
GROUP BY p.player_id,m.format HAVING total_runs>1000 AND total_wickets>50;
-- Q10: Latest completed matches
SELECT m.match_description,t1.team_name team_1,t2.team_name team_2,w.team_name winning_team,m.victory_margin,m.victory_type,v.venue_name
FROM matches m JOIN venues v ON v.venue_id=m.venue_id JOIN match_teams mt1 ON mt1.match_id=m.match_id AND mt1.is_home=1 JOIN teams t1 ON t1.team_id=mt1.team_id
JOIN match_teams mt2 ON mt2.match_id=m.match_id AND mt2.is_home=0 JOIN teams t2 ON t2.team_id=mt2.team_id LEFT JOIN teams w ON w.team_id=m.winning_team_id
WHERE m.status='Completed' ORDER BY m.match_date DESC LIMIT 20;
-- Q11: Cross-format player comparison
SELECT p.full_name, SUM(CASE WHEN m.format='Test' THEN bp.runs ELSE 0 END) test_runs, SUM(CASE WHEN m.format='ODI' THEN bp.runs ELSE 0 END) odi_runs,
SUM(CASE WHEN m.format='T20I' THEN bp.runs ELSE 0 END) t20_runs, ROUND(AVG(bp.runs),2) overall_average, COUNT(DISTINCT m.format) formats_played
FROM players p JOIN batting_performances bp ON bp.player_id=p.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id
GROUP BY p.player_id HAVING formats_played>=2;
-- Q12: Home versus away wins
SELECT t.team_name, CASE WHEN v.country=t.country THEN 'Home' ELSE 'Away' END location, COUNT(*) matches_played,
SUM(CASE WHEN mt.is_winner=1 THEN 1 ELSE 0 END) wins FROM match_teams mt JOIN teams t ON t.team_id=mt.team_id JOIN matches m ON m.match_id=mt.match_id JOIN venues v ON v.venue_id=m.venue_id GROUP BY t.team_id,location;
-- Q13: Consecutive batting partnerships of 100+
SELECT i.innings_id, p1.full_name player_1, p2.full_name player_2, bp1.runs+bp2.runs partnership_runs FROM batting_performances bp1
JOIN batting_performances bp2 ON bp2.innings_id=bp1.innings_id AND bp2.batting_position=bp1.batting_position+1 JOIN innings i ON i.innings_id=bp1.innings_id
JOIN players p1 ON p1.player_id=bp1.player_id JOIN players p2 ON p2.player_id=bp2.player_id WHERE bp1.runs+bp2.runs>=100;
-- Q14: Venue bowling performance
SELECT p.full_name,v.venue_name,COUNT(DISTINCT i.match_id) matches_played,ROUND(AVG(bw.runs_conceded/NULLIF(bw.overs,0)),2) average_economy,SUM(bw.wickets) total_wickets
FROM bowling_performances bw JOIN players p ON p.player_id=bw.player_id JOIN innings i ON i.innings_id=bw.innings_id JOIN matches m ON m.match_id=i.match_id JOIN venues v ON v.venue_id=m.venue_id
WHERE bw.overs>=4 GROUP BY p.player_id,v.venue_id HAVING matches_played>=3;
-- Q15: Close-match batting performance
SELECT p.full_name,ROUND(AVG(bp.runs),2) average_runs,COUNT(DISTINCT m.match_id) close_matches,
SUM(CASE WHEN m.winning_team_id=i.batting_team_id THEN 1 ELSE 0 END) team_wins FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id
WHERE (m.victory_type='runs' AND m.victory_margin<50) OR (m.victory_type='wickets' AND m.victory_margin<5) GROUP BY p.player_id;
-- Q16: Yearly batting performance since 2020
SELECT p.full_name,strftime('%Y',m.match_date) year,ROUND(AVG(bp.runs),2) average_runs,ROUND(AVG(bp.runs*100.0/NULLIF(bp.balls,0)),2) average_strike_rate,COUNT(DISTINCT m.match_id) matches_played
FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id WHERE m.match_date>='2020-01-01' GROUP BY p.player_id,year HAVING matches_played>=5;
-- Q17: Toss advantage
SELECT toss_decision,COUNT(*) matches, SUM(CASE WHEN toss_winner_id=winning_team_id THEN 1 ELSE 0 END) toss_wins_that_won,
ROUND(100.0*SUM(CASE WHEN toss_winner_id=winning_team_id THEN 1 ELSE 0 END)/COUNT(*),2) win_percentage FROM matches WHERE winning_team_id IS NOT NULL GROUP BY toss_decision;
-- Q18: Economical limited-overs bowlers
SELECT p.full_name,ROUND(SUM(bw.runs_conceded)/NULLIF(SUM(bw.overs),0),2) economy_rate,SUM(bw.wickets) total_wickets,COUNT(DISTINCT m.match_id) matches_played
FROM bowling_performances bw JOIN players p ON p.player_id=bw.player_id JOIN innings i ON i.innings_id=bw.innings_id JOIN matches m ON m.match_id=i.match_id WHERE m.format IN ('ODI','T20I')
GROUP BY p.player_id HAVING matches_played>=10 AND SUM(bw.overs)/matches_played>=2 ORDER BY economy_rate;
-- Q19: Consistent batsmen
SELECT p.full_name,ROUND(AVG(bp.runs),2) average_runs,ROUND(sqrt(AVG(bp.runs*bp.runs)-AVG(bp.runs)*AVG(bp.runs)),2) run_stddev,SUM(bp.balls) balls_faced
FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id WHERE bp.balls>=10 AND m.match_date>='2022-01-01' GROUP BY p.player_id ORDER BY run_stddev;
-- Q20: Format participation and averages
SELECT p.full_name,COUNT(DISTINCT CASE WHEN m.format='Test' THEN m.match_id END) test_matches,COUNT(DISTINCT CASE WHEN m.format='ODI' THEN m.match_id END) odi_matches,
COUNT(DISTINCT CASE WHEN m.format='T20I' THEN m.match_id END) t20_matches,ROUND(AVG(CASE WHEN m.format='Test' THEN bp.runs END),2) test_average,
ROUND(AVG(CASE WHEN m.format='ODI' THEN bp.runs END),2) odi_average,ROUND(AVG(CASE WHEN m.format='T20I' THEN bp.runs END),2) t20_average
FROM players p JOIN batting_performances bp ON bp.player_id=p.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id HAVING COUNT(DISTINCT m.match_id)>=20;
-- Q21: Weighted player ranking
WITH bat AS (SELECT p.player_id,p.full_name,m.format,SUM(bp.runs)*0.01+AVG(bp.runs)*0.5+AVG(bp.runs*100.0/NULLIF(bp.balls,0))*0.3 batting_points FROM players p JOIN batting_performances bp ON bp.player_id=p.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id,m.format), bowl AS (SELECT p.player_id,m.format,SUM(bw.wickets)*2+(50-AVG(NULLIF(bw.runs_conceded*1.0/NULLIF(bw.wickets,0),0)))*0.5+(6-AVG(bw.runs_conceded/NULLIF(bw.overs,0)))*2 bowling_points FROM players p JOIN bowling_performances bw ON bw.player_id=p.player_id JOIN innings i ON i.innings_id=bw.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id,m.format), field AS (SELECT player_id,SUM(catches)*3+SUM(stumpings)*5 fielding_points FROM fielding_performances GROUP BY player_id) SELECT bat.full_name,bat.format,ROUND(bat.batting_points+COALESCE(bowl.bowling_points,0)+COALESCE(field.fielding_points,0),2) weighted_score FROM bat LEFT JOIN bowl ON bowl.player_id=bat.player_id AND bowl.format=bat.format LEFT JOIN field ON field.player_id=bat.player_id ORDER BY weighted_score DESC;
-- Q22: Head-to-head pairs
SELECT a.team_id team_a,b.team_id team_b,COUNT(*) matches_played,SUM(CASE WHEN m.winning_team_id=a.team_id THEN 1 ELSE 0 END) team_a_wins,SUM(CASE WHEN m.winning_team_id=b.team_id THEN 1 ELSE 0 END) team_b_wins
FROM match_teams a JOIN match_teams b ON a.match_id=b.match_id AND a.team_id<b.team_id JOIN matches m ON m.match_id=a.match_id WHERE m.match_date>=date('2025-02-15','-3 year') GROUP BY a.team_id,b.team_id HAVING matches_played>=5;
-- Q23: Recent player form (SQLite-compatible last 10 rows)
WITH ranked AS (SELECT p.full_name,bp.runs,bp.balls,m.match_date,ROW_NUMBER() OVER(PARTITION BY p.player_id ORDER BY m.match_date DESC) rn FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id) SELECT full_name,ROUND(AVG(CASE WHEN rn<=5 THEN runs END),2) last_5_average,ROUND(AVG(runs),2) last_10_average,SUM(CASE WHEN runs>=50 THEN 1 ELSE 0 END) scores_over_50,ROUND(AVG(runs*runs)-AVG(runs)*AVG(runs),2) consistency_variance,CASE WHEN AVG(runs)>=80 THEN 'Excellent Form' WHEN AVG(runs)>=50 THEN 'Good Form' WHEN AVG(runs)>=25 THEN 'Average Form' ELSE 'Poor Form' END form_category FROM ranked WHERE rn<=10 GROUP BY full_name;
-- Q24: Successful batting partnerships
SELECT p1.full_name player_1,p2.full_name player_2,COUNT(*) partnership_count,ROUND(AVG(bp1.runs+bp2.runs),2) average_partnership,SUM(CASE WHEN bp1.runs+bp2.runs>50 THEN 1 ELSE 0 END) over_50,MAX(bp1.runs+bp2.runs) highest_partnership,ROUND(100.0*SUM(CASE WHEN bp1.runs+bp2.runs>50 THEN 1 ELSE 0 END)/COUNT(*),2) success_rate
FROM batting_performances bp1 JOIN batting_performances bp2 ON bp2.innings_id=bp1.innings_id AND bp2.batting_position=bp1.batting_position+1 JOIN players p1 ON p1.player_id=bp1.player_id JOIN players p2 ON p2.player_id=bp2.player_id GROUP BY p1.player_id,p2.player_id HAVING partnership_count>=5 ORDER BY success_rate DESC;
-- Q25: Quarterly performance evolution
WITH q AS (SELECT p.full_name,p.player_id,strftime('%Y',m.match_date)||'-Q'||((CAST(strftime('%m',m.match_date) AS INTEGER)-1)/3+1) quarter,AVG(bp.runs) average_runs,AVG(bp.runs*100.0/NULLIF(bp.balls,0)) average_strike_rate,COUNT(*) matches_in_quarter FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id,quarter HAVING matches_in_quarter>=3), trends AS (SELECT *,LAG(average_runs) OVER(PARTITION BY player_id ORDER BY quarter) previous_average FROM q) SELECT full_name,quarter,ROUND(average_runs,2) average_runs,ROUND(average_strike_rate,2) average_strike_rate,CASE WHEN previous_average IS NULL THEN 'Baseline' WHEN average_runs>previous_average+5 THEN 'Improving' WHEN average_runs<previous_average-5 THEN 'Declining' ELSE 'Stable' END quarter_trend FROM trends;
