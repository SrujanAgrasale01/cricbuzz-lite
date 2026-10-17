import os
from pathlib import Path

def test_database_seed(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    import importlib
    import config, db, seed
    importlib.reload(config); importlib.reload(db); importlib.reload(seed)
    seed.seed()
    assert db.query_df("SELECT COUNT(*) n FROM players").iloc[0,0] >= 8
    assert db.query_df("SELECT COUNT(*) n FROM matches").iloc[0,0] >= 5

def test_player_crud(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    import importlib
    import config, db, seed
    importlib.reload(config); importlib.reload(db); importlib.reload(seed)
    seed.seed()
    before = len(db.list_players("Test"))
    db.create_player("Test Player", "India", "Batsman", "Right-hand", "Right-arm medium")
    assert len(db.list_players("Test")) == before + 1
