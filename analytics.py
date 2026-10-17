"""Registry and execution helper for the 25 SQL analytics questions."""
from pathlib import Path
import re
from db import query_df

QUERY_FILE = Path(__file__).parent / "sql" / "queries.sql"

def load_queries() -> dict[int, str]:
    text = QUERY_FILE.read_text(encoding="utf-8")
    chunks = re.split(r"(?=-- Q\d+:)", text)
    queries = {}
    for chunk in chunks:
        match = re.match(r"-- Q(\d+):", chunk.strip())
        if match:
            number = int(match.group(1))
            sql = chunk.split("\n", 1)[1].strip().rstrip(";")
            queries[number] = sql
    return queries

def run_query(number: int):
    return query_df(load_queries()[number])
