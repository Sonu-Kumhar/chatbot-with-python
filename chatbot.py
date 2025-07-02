# rapid_chatbot.py
import os, requests, json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

RAPID_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPID_KEY:
    raise EnvironmentError("Missing RAPIDAPI_KEY in .env file")

# (Quick test only … you could instead do: RAPID_KEY = "10ec200bbb..." )

# 2 ── Endpoint info from your cURL snippet
URL = "https://chatgpt-42.p.rapidapi.com/chat"
HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": RAPID_KEY,
    "X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com"
}
MODEL_NAME = "gpt-4o-mini"

chat_history = []   # keep short context

print("RapidAPI GPT-4o-mini chatbot ready.  Type 'quit' to exit.\n")

# 3 ── Chat loop
while True:
    user = input("You   : ")
    if user.lower() in {"quit", "exit"}:
        print("Bot   : Bye!")
        break

    chat_history.append({"role": "user", "content": user})

    payload = {
        "model": MODEL_NAME,
        "messages": chat_history[-10:]   # send last 10 exchanges for context
    }

    try:
        response = requests.post(URL, json=payload, headers=HEADERS, timeout=20)
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        bot_reply = f"(RapidAPI error: {e})"

    chat_history.append({"role": "assistant", "content": bot_reply})
    print("Bot   :", bot_reply, "\n")
