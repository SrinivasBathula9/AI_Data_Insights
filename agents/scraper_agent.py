from playwright.sync_api import sync_playwright
import pandas as pd
import logging
import yfinance as yf
from config import settings

logger = logging.getLogger(__name__)

def fetch_trending_tickers() -> pd.DataFrame:
    """
    Fetches trending tickers using yfinance.
    """
    try:
        logger.info("Fetching trending tickers using yfinance...")
        # Since yfinance's trending API can be unstable, we'll fetch data for 
        # a set of predefined popular tickers as a demonstration of "structured data"
        # In a real scenario, this list could be dynamic.
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX"]
        data = []
        for symbol in tickers:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            data.append({
                "Symbol": symbol,
                "Name": info.get("longName", "N/A"),
                "Price": info.get("currentPrice", "N/A"),
                "Change": info.get("regularMarketChangePercent", "N/A"),
                "Volume": info.get("regularMarketVolume", "N/A"),
                "Description": info.get("longBusinessSummary", "N/A")[:500] + "..." # Limit text
            })
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching trending tickers: {e}")
        return pd.DataFrame()

def scrape_data(url: str = settings.DEFAULT_SCRAPE_URL) -> pd.DataFrame:
    """
    Scrapes data from the given URL. Prefers yfinance for Yahoo Finance.
    """
    if "finance.yahoo.com" in url:
        df = fetch_trending_tickers()
        if not df.empty:
            return df

    # Fallback to Playwright for other URLs
    results = []
    logger.info(f"Starting fallback scrape for URL: {url}")
    # ... rest of the original scrape_data logic ...
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(settings.PAGE_TIMEOUT)
            page.goto(url, wait_until="domcontentloaded")
            items = page.locator(".item").all_text_contents()
            for item in items:
                results.append({"text": item})
            browser.close()
    except Exception as e:
        logger.error(f"Fallback scrape failed: {e}")
        return pd.DataFrame(columns=["text"])

    return pd.DataFrame(results)
