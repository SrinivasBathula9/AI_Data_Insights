import logging
import sys
from config import settings
from agents.scraper_agent import scrape_data
from agents.transform_agent import clean_data
from agents.insight_agent import generate_insights
from database.db import save_to_db

# Configure Logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log")
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline(url: str = settings.DEFAULT_SCRAPE_URL):
    """
    Executes the full data insight pipeline.
    """
    logger.info("Starting AI Data Insight Pipeline...")
    
    try:
        # 1. Scrape
        logger.info("Phase 1: Scrape")
        raw_data = scrape_data(url)
        if raw_data.empty:
            logger.error("No data scraped. Terminating pipeline.")
            return

        # 2. Transform
        logger.info("Phase 2: Transform")
        cleaned_data = clean_data(raw_data)

        # 3. Save to Database
        logger.info("Phase 3: Database Storage")
        save_to_db(cleaned_data)

        # 4. Generate Insights
        logger.info("Phase 4: AI Insights")
        insights = generate_insights(cleaned_data)
        
        # 5. Save Insights to DB
        from database.db import save_insights
        save_insights(insights)
        
        logger.info("Pipeline completed successfully.")
        print("\n" + "="*50)
        print("AI INSIGHTS")
        print("="*50)
        print(insights)
        print("="*50 + "\n")

    except Exception as e:
        logger.critical(f"Pipeline failed with an unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    run_pipeline()
