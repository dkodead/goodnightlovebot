# 💌 Goodnight LoveBot

A mood-driven, WhatsApp-sending love bot designed to help you never miss saying goodnight to someone special — even if you're tired, busy, or just feeling a little off.

This is a self-hosted Flask web app (Docker-ready) that asks *you* how you're feeling each day. Based on your mood and reflections, it sends your girlfriend a personalized goodnight message via WhatsApp at 10 PM every night.

---

## ✨ Features

- 🧠 Mood tracking: Select your mood and optionally leave a note about your day or thoughts for her.
- 💬 Automatic messaging: A sweet goodnight WhatsApp message gets sent each night.
- 🎭 Interface switcher: Choose between a **classic form UI** or a **terminal-style experience**.
- 🐳 Fully Dockerized: Easy to run anywhere, no local Python setup required.
- 💬 Twilio + WhatsApp Business API integration.

---

## 🧰 Technologies Used

- Python 3.11
- Flask
- APScheduler
- SQLite
- Twilio WhatsApp API
- Docker

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/dkodead/goodnightlovebot.git
cd goodnightlovebot
