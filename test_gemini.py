import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000)
)

print("Connecting to Gemini...", flush=True)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello to the AI Escape Room player."
    )

    print("Gemini Response:")
    print(response.text)

except Exception as e:
    print("Error:", type(e).__name__, str(e))