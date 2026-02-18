from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import duckdb
import pandas as pd
from config import settings
import os

app = FastAPI(title="AI Data Insight Hybrid Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def get_ui():
    try:
        with open("standalone_ui.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading UI: {str(e)}</h1>"

@app.get("/data")
def get_data():
    db_path = str(settings.DATABASE_PATH)
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="Database not found")
    
    try:
        with duckdb.connect(db_path) as con:
            df = con.execute("SELECT * FROM data").fetchdf()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights")
def get_insights():
    db_path = str(settings.DATABASE_PATH)
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="Database not found")
    
    try:
        with duckdb.connect(db_path) as con:
            # Check if insights table exists
            table_exists = con.execute(
                "SELECT count(*) FROM information_schema.tables WHERE table_name = 'insights'"
            ).fetchone()[0] > 0
            
            if not table_exists:
                return {"content": "Insights not yet generated."}
                
            insight = con.execute("SELECT content, generated_at FROM insights ORDER BY generated_at DESC LIMIT 1").fetchone()
            if insight:
                return {"content": insight[0], "generated_at": insight[1]}
            return {"content": "No insights found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
