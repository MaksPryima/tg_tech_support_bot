from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
TRIGGER_TAG = "#important"

def send_pushover_notification(text):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": text,
        "priority": 1,
        "sound": "siren"
    })

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    try:
        message = data.get("message", {})
        text = message.get("text", "")
        if TRIGGER_TAG in text:
            user = message.get("from", {}).get("first_name", "Unknown")
            chat = message.get("chat", {})
            chat_username = chat.get("username")
            message_id = message.get("message_id")

            link = f"https://t.me/{chat_username}/{message_id}" if chat_username else f"(no link, id {message_id})"
            alert = f"🚨 {user}: {text}\n🔗 {link}"
            send_pushover_notification(alert)
    except Exception as e:
        print("Error:", e)

    return {"ok": True}

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
