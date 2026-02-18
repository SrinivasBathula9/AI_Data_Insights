import google.generativeai as genai
import os
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

with open("d:/ML/Agentic AI/AI_Data_Insights/models_detected.txt", "w") as f:
    try:
        f.write("Fetching models...\n")
        for m in genai.list_models():
            f.write(f"{m.name}\n")
        f.write("Done.\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
