import streamlit as st
import duckdb
import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to sys.path for absolute imports
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from config import settings

st.set_page_config(page_title="AI Data Insights", layout="wide")

st.title("🚀 AI Data Insights Dashboard")

db_path = str(settings.DATABASE_PATH)

if not os.path.exists(db_path):
    st.error(f"Database not found at {db_path}. Please run the pipeline first.")
else:
    try:
        with duckdb.connect(db_path) as con:
            df = con.execute("SELECT * FROM data").fetchdf()

        if df.empty:
            st.warning("Database is empty. No data to display.")
        else:
            # 1. AI Insights Section (Prominent)
            try:
                with duckdb.connect(db_path) as con:
                    insight_df = con.execute("SELECT content FROM insights ORDER BY generated_at DESC LIMIT 1").fetchdf()
                if not insight_df.empty:
                    content = insight_df['content'].iloc[0]
                    st.success("🤖 AI Strategic Analysis")
                    
                    # Parsing Logic
                    lines = content.split('\n')
                    direction = next((l for l in lines if "MARKET DIRECTION" in l), "").split(":")[-1].strip()
                    sentiment = next((l for l in lines if "Sentiment:" in l), "").split(":")[-1].strip()
                    risk = next((l for l in lines if "Risk Level:" in l), "").split(":")[-1].strip()
                    takeaways = [l.replace("- ", "").strip() for l in lines if l.strip().startswith("- ")]

                    # UI Layout
                    col_dir, col_meta = st.columns([2, 1])
                    with col_dir:
                        st.info(f"**Executive Summary**\n\n{direction}")
                    with col_meta:
                        st.metric("Sentiment", sentiment)
                        st.metric("Portfolio Risk", risk)

                    if takeaways:
                        st.markdown("### 💡 Strategic Takeaways")
                        t_cols = st.columns(len(takeaways[:3]))
                        for idx, takeaway in enumerate(takeaways[:3]):
                             with t_cols[idx]:
                                 st.warning(takeaway)
                    
                    st.divider()
            except Exception as e:
                st.info("AI insights not yet available.")

            # 2. Key Metrics
            st.subheader("📊 Key Market Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Stocks Tracked", len(df))
            with col2:
                if "Price" in df.columns and pd.to_numeric(df["Price"], errors='coerce').notnull().all():
                    avg_price = pd.to_numeric(df["Price"], errors='coerce').mean()
                    st.metric("Avg Stock Price", f"${avg_price:.2f}")
                else:
                    st.metric("Data Points", len(df))
            with col3:
                if "Change" in df.columns:
                    top_performer = df.loc[pd.to_numeric(df["Change"], errors='coerce').idxmax()]["Symbol"]
                    st.metric("Top Gainer", top_performer)
                else:
                    st.metric("Unique Items", df.iloc[:, 0].nunique())

            # 3. Data Table
            st.subheader("📈 Detailed Market Data")
            st.dataframe(df, use_container_width=True)

            # 4. Visualization
            if "Change" in df.columns:
                st.subheader("Price Changes (%)")
                chart_data = df.set_index("Symbol")["Change"]
                st.bar_chart(pd.to_numeric(chart_data, errors='coerce'))
            
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
