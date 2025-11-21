import os
import requests
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your Gemini 3 Pro API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Gemini 3.0 Pro Model Name
MODEL = "models/gemini-3.0-flash"

@app.post("/chat")
async def chat(message: str = Form(...)):
    if not GEMINI_API_KEY:
        return {"reply": "ERROR: Gemini API key not set on server"}

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=body)
        data = res.json()

        if "error" in data:
            return {"reply": "GEMINI ERROR: " + data["error"]["message"]}

        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Server Error: {str(e)}"}
