import pandas as pd
from pathlib import Path

from app.db import get_conn, init_db

Required_columns = {"date", "app_id", "region", "transactions", "revenue", "avg_rating"}


def validate_df(df: pd.DataFrame) -> None:
    """Validate that the DataFrame contains the required columns."""
    
    missing = Required_columns - set(df.columns)
    if missing:
        # If something is missing there will be an error made
        raise ValueError(f"Missing required columns: {sorted(missing)}")
        # Makes sure there is no empty values in the required columns
    if df[["date", "app_id", "region"]].isnull().any().any():
        raise ValueError("Columns 'date', 'app_id', and 'region' cannot contain null values.")

    if (df[["transactions"]] < 0).any().any():
        raise ValueError("Negative transactions found")

    if (df[["revenue"]] < 0).any().any():
        raise ValueError("Negative revenue found")

    if ((df["avg_rating"] < 1.0) | (df["avg_rating"] > 5.0)).any():
        raise ValueError("avg_rating out of range 1-5")
    
def ingest_csv(file_path: Path) -> None:
    """Ingest a CSV file into the database."""
    # Initialize the database, which will create tables if they don't exist
    init_db()
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)  
    # Validate the DataFrame
    validate_df(df) 
    # Insert data into the database
    with get_conn() as conn:
        df.to_sql("metrics", conn, if_exists="append", index=False)
