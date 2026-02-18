import duckdb
import pandas as pd
import logging
from config import settings

logger = logging.getLogger(__name__)

def save_to_db(df: pd.DataFrame, table_name: str = "data"):
    """
    Saves the DataFrame to the DuckDB database.
    
    Args:
        df (pd.DataFrame): The DataFrame to save.
        table_name (str): The name of the table.
    """
    if df.empty:
        logger.warning(f"Attempted to save empty DataFrame to {table_name}.")
        return

    db_path = str(settings.DATABASE_PATH)
    logger.info(f"Saving data to table '{table_name}' in {db_path}...")

    try:
        # Use context manager for implicit connection closing
        with duckdb.connect(db_path) as con:
            # Check if table exists
            table_exists = con.execute(
                f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
            ).fetchone()[0] > 0
            
            if table_exists:
                logger.info(f"Table '{table_name}' exists. Appending or updating data...")
                # Note: For simplicity, we overwrite in this basic pipeline, 
                # but could use INSERT for appending.
                con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            else:
                con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
                
        logger.info(f"Successfully saved to {table_name}.")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise

def save_insights(insights: str):
    """
    Saves the AI-generated insights to a dedicated table.
    """
    db_path = str(settings.DATABASE_PATH)
    logger.info(f"Saving AI insights to {db_path}...")
    
    try:
        with duckdb.connect(db_path) as con:
            con.execute("CREATE OR REPLACE TABLE insights (content TEXT, generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            con.execute("INSERT INTO insights (content) VALUES (?)", [insights])
        logger.info("Successfully saved insights.")
    except Exception as e:
        logger.error(f"Error saving insights: {e}")
