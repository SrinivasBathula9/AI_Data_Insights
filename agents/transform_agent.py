import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms the scraped data.
    """
    if df.empty:
        logger.warning("Cleaning requested on empty DataFrame.")
        return df

    logger.info(f"Processing {len(df)} rows of data.")
    
    # Remove duplicates
    df = df.drop_duplicates()

    # If it's structured stock data, ensure columns are clean
    if "Symbol" in df.columns:
        # Fill missing values
        df = df.fillna("N/A")
        logger.info("Structured stock data detected and cleaned.")
    
    # Add length column for text data if present
    if "text" in df.columns:
        df["length"] = df["text"].str.len()
    
    return df

def format_data_for_insights(df: pd.DataFrame) -> str:
    """
    Converts the DataFrame into a readable string format for the AI agent.
    """
    if df.empty:
        return "No data available."
    
    if "Symbol" in df.columns:
        # Create a summary of the stock data
        summary = "Market Data Summary:\n"
        for _, row in df.iterrows():
            summary += f"- {row['Symbol']} ({row['Name']}): Price ${row['Price']}, Change {row['Change']}%, Volume {row['Volume']}\n"
            summary += f"  Summary: {row['Description']}\n\n"
        return summary
    
    # Fallback to simple text join
    if "text" in df.columns:
        return "\n".join(df["text"].tolist())
    
    return str(df.to_dict(orient="records"))
