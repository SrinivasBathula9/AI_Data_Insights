from agents.scraper_agent import fetch_trending_tickers
from agents.transform_agent import clean_data, format_data_for_insights
from agents.insight_agent import generate_insights

print("Phase 1: Scrape (yfinance)")
df = fetch_trending_tickers()
print(f"Scraped {len(df)} tickers")

print("Phase 2: Transform")
cleaned = clean_data(df)
formatted = format_data_for_insights(cleaned)
print("Data formatted for insights")

print("Phase 3: Insights")
insights = generate_insights(cleaned)
print("Insights generated:")
print(insights)
