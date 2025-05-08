from flask import Flask, request, render_template, redirect, session, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import init_db, get_today_mood, save_mood, save_context, get_context
from message_generator import generate_message
import os
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path="/home/dkoded/Development/goodnightlovebot/.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "defaultsecret")
init_db()

# Configuration
WHATSAPP_TO = os.getenv("WHATSAPP_TO")
DEFAULT_CONTEXT = os.getenv("DEFAULT_CONTEXT", "")
WHATSAPP_SENDER_URL = os.getenv("WHATSAPP_SENDER_URL", "http://localhost:3000/send")

@app.route("/", methods=["GET", "POST"])
def index():
    view = session.get("view", "gui")
    if request.args.get("view"):
        session["view"] = request.args.get("view")
        return redirect("/")

    today = datetime.now().date()
    stored_context = get_context() or DEFAULT_CONTEXT
    today_mood = get_today_mood(today)

    if request.method == "POST":
        mood = request.form.get("mood")
        note = request.form.get("note", "")
        context = request.form.get("context", stored_context)
        print(f"[INFO] Received mood submission: mood={mood}, note={note}, context={context}")

        if mood:
            save_mood(today, mood, note)
        if context:
            save_context(context)
        return redirect("/")

    print(f"[INFO] Fetched today's mood: {today_mood}")
    template = "index.html" if view == "gui" else "terminal.html"
    return render_template(template, mood=today_mood, context=stored_context)

@app.route("/context", methods=["GET", "POST"])
def update_context():
    if request.method == "POST":
        new_context = request.form.get("context")
        if new_context:
            print(f"[INFO] Context update received: {new_context}")
            save_context(new_context)
            return jsonify({"status": "success", "message": "Context updated."})
        return jsonify({"status": "error", "message": "No context provided."}), 400

    current_context = get_context() or DEFAULT_CONTEXT
    return jsonify({"context": current_context})

def send_whatsapp_message(message, recipient=None):
    recipient = recipient or WHATSAPP_TO
    try:
        response = requests.post(WHATSAPP_SENDER_URL, json={
            "to": f"{recipient}",
            "message": message
        })
        response.raise_for_status()
        print(f"[INFO] Message successfully sent via local WhatsApp sender to {recipient}.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to send message: {e}")

def gn():
    today = datetime.now().date()
    print(f"[INFO] Running nightly message task for date: {today}")
    mood_data = get_today_mood(today)
    print(f"[INFO] Retrieved mood data: {mood_data}")
    session_context = get_context() or ""
    print(f"[INFO] Using session context: {session_context}")
    message = generate_message(mood_data, DEFAULT_CONTEXT, session_context)
    print(f"[INFO] Generated message: {message}")
    send_whatsapp_message(message)

@app.route("/test-send")
def test_gn():
    print("[TEST] Running test message send...")
    test_message = generate_message(("test", "this is a test context"), DEFAULT_CONTEXT, "Test context only.")
    send_whatsapp_message(test_message, recipient="null@c.us")
    return jsonify({"status": "test sent", "message": test_message})

scheduler = BackgroundScheduler()
scheduler.add_job(gn(), 'cron', hour=22, minute=0)
scheduler.start()

if __name__ == "__main__":
    print("[INFO] Starting Flask app on port 5000")
    app.run(host="0.0.0.0", port=5000)
