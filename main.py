import os
import telebot
import requests
from flask import Flask, request
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

CHARACTER = "তুমি একজন কামুক এলফ রাজকুমারী। তুমি কোমল, রোমান্টিক, একটু খোলামেলা কথা বলো।"

@app.route('/')
def index():
    return "Fantasy Telegram Bot is Running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! Fantasy chat করতে কিছু লিখুন।")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_input = message.text.strip()
    prompt = f"Character: {CHARACTER}\nUser: {user_input}\nAI:"
    response = generate_ai_response(prompt)
    bot.reply_to(message, response)

def generate_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openrouter/openhermes-2.5-mistral",
        "messages": [
            {"role": "system", "content": CHARACTER},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI এর সাথে সংযোগ ব্যর্থ: {e}"

def start_polling():
    bot.infinity_polling()

# Flask app চালু হলে আলাদা থ্রেডে টেলিগ্রাম বট চালু হবে
if __name__ == "__main__":
    threading.Thread(target=start_polling).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
