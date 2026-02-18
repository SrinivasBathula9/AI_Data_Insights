import google.generativeai as genai
import os
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}, Display Name: {m.display_name}")
except Exception as e:
    print(f"Error listing models: {e}")
