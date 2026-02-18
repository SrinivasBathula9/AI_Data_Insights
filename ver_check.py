import sys
print(sys.version)
try:
    import google.generativeai as genai
    print("Gemini SDK installed")
except ImportError:
    print("Gemini SDK NOT installed")
