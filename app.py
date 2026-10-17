"""Streamlit dashboard for Cricbuzz LiveStats."""
import streamlit as st
import pandas as pd
from analytics import load_queries, run_query
from api_client import CricketAPIClient, CricketAPIError
from db import initialize_database, list_players, create_player, update_player, delete_player, query_df
from config import settings

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")
initialize_database()
if settings.auto_seed_demo_data and int(query_df("SELECT COUNT(*) AS total FROM teams").iloc[0]["total"]) == 0:
    from seed import seed
    seed()

@st.cache_data(ttl=30)
def local_live_matches():
    return query_df("""SELECT match_description, format, match_date, status, venue_name, city,
                      t1.team_name AS team_1, t2.team_name AS team_2, wt.team_name AS winner,
                      victory_margin, victory_type
                      FROM matches m JOIN venues v ON v.venue_id=m.venue_id
                      JOIN match_teams mt1 ON mt1.match_id=m.match_id AND mt1.is_home=1
                      JOIN teams t1 ON t1.team_id=mt1.team_id
                      JOIN match_teams mt2 ON mt2.match_id=m.match_id AND mt2.is_home=0
                      JOIN teams t2 ON t2.team_id=mt2.team_id
                      LEFT JOIN teams wt ON wt.team_id=m.winning_team_id
                      ORDER BY match_date DESC""")

def home():
    st.title("🏏 Cricbuzz LiveStats")
    st.subheader("Real-time cricket insights and SQL-based analytics")
    st.write("A modular learning project combining REST APIs, relational SQL, Python, and Streamlit.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Matches", int(query_df("SELECT COUNT(*) n FROM matches").iloc[0,0]))
    c2.metric("Players", int(query_df("SELECT COUNT(*) n FROM players").iloc[0,0]))
    c3.metric("Teams", int(query_df("SELECT COUNT(*) n FROM teams").iloc[0,0]))
    c4.metric("SQL exercises", 25)
    st.info("Use the sidebar to explore live matches, player statistics, SQL analytics, and CRUD operations.")
    st.markdown("### Architecture")
    st.code("API → validation/normalization → SQL database → services/analytics → Streamlit UI", language="text")

def live_matches():
    st.title("Live Matches")
    client = CricketAPIClient()
    if not client.configured:
        st.warning(f"{client.configuration_message} Local seeded data is shown below.")
    elif st.button("Refresh from configured API"):
        try:
            payload = client.live_matches()
            normalized = client.normalize_live_matches(payload)
            st.success(f"API response received: {len(normalized)} match record(s) detected.")
            if normalized:
                st.dataframe(pd.DataFrame(normalized), use_container_width=True, hide_index=True)
            else:
                st.info("The request succeeded, but no match list was found in the response wrapper.")
            with st.expander("Show raw provider response"):
                st.json(payload)
        except CricketAPIError as exc:
            st.error(f"API request failed: {exc}")
    if client.configured:
        st.markdown("### Match scorecard")
        match_id = st.text_input("Provider match ID", value="40381", help="Example RapidAPI match ID: 40381")
        if st.button("Fetch scorecard"):
            try:
                scorecard = client.scorecard(match_id)
                st.success(f"Scorecard received for match {match_id}.")
                st.json(scorecard)
            except CricketAPIError as exc:
                st.error(f"Scorecard request failed: {exc}")
    st.caption("Local seeded data remains available as a fallback and for SQL practice.")
    st.dataframe(local_live_matches(), use_container_width=True, hide_index=True)

def top_stats():
    st.title("Top Player Stats")
    format_choice = st.selectbox("Format", ["All", "Test", "ODI", "T20I"])
    where = "" if format_choice == "All" else "WHERE m.format = ?"
    params = () if not where else (format_choice,)
    batting = query_df(f"""SELECT p.full_name, SUM(bp.runs) total_runs,
        ROUND(AVG(CASE WHEN bp.not_out=0 THEN bp.runs END),2) batting_average,
        SUM(CASE WHEN bp.runs>=100 THEN 1 ELSE 0 END) centuries
        FROM batting_performances bp JOIN players p ON p.player_id=bp.player_id
        JOIN innings i ON i.innings_id=bp.innings_id JOIN matches m ON m.match_id=i.match_id
        {where} GROUP BY p.player_id ORDER BY total_runs DESC LIMIT 10""", params)
    bowling = query_df(f"""SELECT p.full_name, SUM(bw.wickets) wickets,
        ROUND(SUM(bw.runs_conceded)/NULLIF(SUM(bw.overs),0),2) economy_rate
        FROM bowling_performances bw JOIN players p ON p.player_id=bw.player_id
        JOIN innings i ON i.innings_id=bw.innings_id JOIN matches m ON m.match_id=i.match_id
        {where} GROUP BY p.player_id ORDER BY wickets DESC LIMIT 10""", params)
    st.subheader("Top batters"); st.dataframe(batting, use_container_width=True, hide_index=True)
    st.subheader("Top bowlers"); st.dataframe(bowling, use_container_width=True, hide_index=True)
    if not batting.empty: st.bar_chart(batting.set_index("full_name")["total_runs"])

def analytics_page():
    st.title("SQL Queries & Analytics")
    queries = load_queries()
    number = st.selectbox("Choose question", sorted(queries), format_func=lambda n: f"Q{n}")
    st.code(queries[number], language="sql")
    try:
        result = run_query(number)
        st.dataframe(result, use_container_width=True, hide_index=True)
        st.caption(f"Returned {len(result)} rows.")
    except Exception as exc:
        st.error(f"Query failed: {exc}")

def crud_page():
    st.title("Player CRUD")
    players = list_players(st.text_input("Search players"))
    st.dataframe(players, use_container_width=True, hide_index=True)
    with st.expander("Create player"):
        with st.form("create_player"):
            name=st.text_input("Full name"); country=st.text_input("Country")
            role=st.selectbox("Role", ["Batsman","Bowler","All-rounder","Wicket-keeper"])
            bat=st.text_input("Batting style", "Right-hand"); bowl=st.text_input("Bowling style", "Right-arm medium")
            if st.form_submit_button("Create"):
                try: create_player(name,country,role,bat,bowl); st.success("Player created"); st.rerun()
                except Exception as exc: st.error(str(exc))
    if not players.empty:
        selected = st.selectbox("Select player to update/delete", players.player_id.tolist(), format_func=lambda x: players.loc[players.player_id==x,"full_name"].iloc[0])
        row = players[players.player_id==selected].iloc[0]
        with st.form("update_player"):
            name=st.text_input("Name", row.full_name); country=st.text_input("Country", row.country)
            role=st.selectbox("Role", ["Batsman","Bowler","All-rounder","Wicket-keeper"], index=["Batsman","Bowler","All-rounder","Wicket-keeper"].index(row.playing_role))
            bat=st.text_input("Batting style", row.batting_style or ""); bowl=st.text_input("Bowling style", row.bowling_style or "")
            if st.form_submit_button("Update"):
                try: update_player(int(selected),name,country,role,bat,bowl); st.success("Player updated"); st.rerun()
                except Exception as exc: st.error(str(exc))
        if st.button("Delete selected player", type="secondary"):
            try: delete_player(int(selected)); st.success("Player deleted"); st.rerun()
            except Exception as exc: st.error(f"Delete failed: {exc}")

def main():
    page = st.sidebar.radio("Navigate", ["Home", "Live Matches", "Top Player Stats", "SQL Analytics", "Player CRUD"])
    {"Home":home,"Live Matches":live_matches,"Top Player Stats":top_stats,"SQL Analytics":analytics_page,"Player CRUD":crud_page}[page]()

if __name__ == "__main__": main()
