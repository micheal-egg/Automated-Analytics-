#This will be used to create the connection and open databases

import sqlite3
from pathlib import Path 

# This will define the path to the SQL DB file
DB_PATH = Path("app") / "analytics.db"

# Function to get a connection to the database
def get_conn() -> sqlite3.Connection:
    # If the directory does not exist, create it
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    # Row factory will return stuff as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

# This will create the database and return nothing
def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            date TEXT NOT NULL,
            app_id TEXT NOT NULL,
            region TEXT NOT NULL,
            transactions INTEGER NOT NULL,
            revenue REAL NOT NULL,
            avg_rating REAL NOT NULL
        );
        """)
        # I use Index on Dates for faster queries
        conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_date ON metrics(date);")