import requests
import os

def generate_message(mood_data, default_context, session_context):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/home/dkoded/Development/goodnightlovebot/.env")
    combined_context = f"{default_context}\n{session_context}".strip()
    if not mood_data:
        prompt = combined_context + "\nWrite a short, sweet goodnight message for my girlfriend."
    else:
        mood, note = mood_data
        prompt = (
            combined_context + "\n"
            f"Today I felt {mood}. I want to tell her: '{note}'. "
            "Please generate a heartfelt, short goodnight message based on this."
        )

    print(f"[INFO] Sending prompt to Mistral LLM:\n{prompt}")

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        message = response.json().get("response", "").strip()
        print(f"[INFO] LLM generated message: {message}")
        return message
    except Exception as e:
        print(f"[ERROR] Failed to get response from Mistral: {e}")
        return "Goodnight my love ❤️ I hope today was gentle on your heart. Sweet dreams schatje."
