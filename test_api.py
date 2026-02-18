import requests
try:
    data_res = requests.get("http://localhost:8000/data")
    print(f"Data Endpoint Status: {data_res.status_code}")
    print(f"Data Sample: {data_res.json()[:1]}")
    
    insight_res = requests.get("http://localhost:8000/insights")
    print(f"Insights Endpoint Status: {insight_res.status_code}")
    print(f"Insights Sample: {insight_res.json().get('content')[:50]}...")
except Exception as e:
    print(f"Error checking API: {e}")
