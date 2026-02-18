import google.generativeai as genai
import pandas as pd
import logging
from config import settings
from agents.transform_agent import format_data_for_insights

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_insights(df: pd.DataFrame) -> str:
    """
    Generates AI insights from the data summary using Gemini.
    """
    if df.empty:
        logger.warning("Insight generation requested for empty DataFrame.")
        return "No data available to analyze."

    logger.info("Generating AI insights using Gemini...")
    
    # Use the formatted data string
    formatted_data = format_data_for_insights(df)

    prompt = f"""
    You are a professional financial analyst. Based on the following stock market data, provide a structured, high-impact summary for business executives.
    
    Data:
    {formatted_data}
    
    CRITICAL: You MUST format your response exactly as follows using these headers:
    
    1. **MARKET DIRECTION**: A single powerful sentence summarizing the overall trend.
    2. **STRATEGIC TAKEAWAYS**: 3 punchy, actionable bullet points (prefix each with '- ').
    3. **SENTIMENT & RISK**: 
       - Sentiment: [Bullish/Bearish/Neutral]
       - Risk Level: [Low/Medium/High]
    """

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(prompt)
        insights = response.text
        logger.info("Insights generated successfully.")
        return insights
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return f"Failed to generate insights: {e}"
