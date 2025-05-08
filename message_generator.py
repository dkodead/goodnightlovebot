def generate_message(mood_data):
    print(f"[INFO] Generating message for mood data: {mood_data}")
    if not mood_data:
        return "Goodnight my love ❤️ I hope today was gentle on your heart. Sleep peacefully."

    mood, note = mood_data
    if mood == "sad":
        return "I know today was hard 😔 but I'm here with you in spirit. Sleep easy, my heart."
    elif mood == "ok":
        return "Another day done. I'm proud of you, babe. Rest up 😌💤"
    elif mood == "happy":
        return "You're glowing brighter than the moon tonight ✨ Sweet dreams my love 💋"
    else:
        return f"Goodnight sweetheart ❤️ Today you felt: {mood}. I’m thinking of you always."
