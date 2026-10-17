"""SQLite persistence, schema initialization, CRUD, and query execution."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Any, Iterable
from config import settings

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

@contextmanager
def get_connection():
    settings.ensure_data_dir()
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

def query_df(sql: str, params: Iterable[Any] = ()):
    import pandas as pd
    with get_connection() as connection:
        return pd.read_sql_query(sql, connection, params=tuple(params))

def execute(sql: str, params: Iterable[Any] = ()) -> int:
    with get_connection() as connection:
        cursor = connection.execute(sql, tuple(params))
        return cursor.rowcount

def list_players(search: str = ""):
    sql = "SELECT * FROM players WHERE full_name LIKE ? ORDER BY full_name"
    return query_df(sql, (f"%{search}%",))

def create_player(full_name: str, country: str, role: str, batting_style: str, bowling_style: str) -> None:
    if not full_name.strip() or not country.strip():
        raise ValueError("Full name and country are required")
    execute("""INSERT INTO players(full_name,country,playing_role,batting_style,bowling_style)
               VALUES (?,?,?,?,?)""", (full_name.strip(), country.strip(), role, batting_style, bowling_style))

def update_player(player_id: int, full_name: str, country: str, role: str, batting_style: str, bowling_style: str) -> None:
    if not full_name.strip() or not country.strip():
        raise ValueError("Full name and country are required")
    execute("""UPDATE players SET full_name=?, country=?, playing_role=?, batting_style=?, bowling_style=?
              WHERE player_id=?""", (full_name.strip(), country.strip(), role, batting_style, bowling_style, player_id))

def delete_player(player_id: int) -> None:
    execute("DELETE FROM players WHERE player_id=?", (player_id,))
