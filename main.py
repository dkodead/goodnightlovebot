from flask import Flask, request, render_template, redirect, session
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import init_db, get_today_mood, save_mood
from message_generator import generate_message
from twilio.rest import Client
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "defaultsecret")
init_db()

# Twilio config (from .env or Docker secrets)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/", methods=["GET", "POST"])
def index():
    view = session.get("view", "gui")
    if request.args.get("view"):
        session["view"] = request.args.get("view")
        return redirect("/")

    if request.method == "POST":
        mood = request.form["mood"]
        note = request.form.get("note", "")
        print(f"[INFO] Received mood submission: mood={mood}, note={note}")
        save_mood(datetime.now().date(), mood, note)
        return redirect("/")

    today_mood = get_today_mood(datetime.now().date())
    print(f"[INFO] Fetched today's mood: {today_mood}")
    template = "index.html" if view == "gui" else "terminal.html"
    return render_template(template, mood=today_mood)

def send_nightly_message():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/full/path/to/your/.env")  # Use your absolute path here

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
    WHATSAPP_TO = os.getenv("WHATSAPP_TO")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    today = datetime.now().date()
    print(f"[INFO] Running nightly message task for date: {today}")
    mood_data = get_today_mood(today)
    print(f"[INFO] Retrieved mood data: {mood_data}")
    message = generate_message(mood_data)
    print(f"[INFO] Generated message: {message}")
    client.messages.create(
        body=message,
        from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
        to=f"whatsapp:{WHATSAPP_TO}"
    )
    print("[INFO] WhatsApp message sent successfully.")

scheduler = BackgroundScheduler()
scheduler.add_job(send_nightly_message, 'cron', hour=22, minute=0)  # 10 PM
scheduler.start()

if __name__ == "__main__":
    print("[INFO] Starting Flask app on port 5000")
    app.run(host="0.0.0.0", port=5000)
