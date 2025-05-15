import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def generate_ai_response(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openhermes-2.5-mistral",  # আপনি চাইলে এখানে অন্য মডেল ব্যবহার করতে পারেন
        "messages": [
            {"role": "system", "content": "You are a seductive elf princess in a romantic fantasy world. Be playful, gentle, and imaginative."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "আমি এখন কিছু বলতে পারছি না, একটু পরে বলো।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! Fantasy chat করতে /chat এর পর কিছু লিখুন।")

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    user_input = message.text.replace("/chat", "").strip()
    if not user_input:
        bot.reply_to(message, "দয়া করে /chat এর পর কিছু লিখুন।")
        return
    response = generate_ai_response(user_input)
    bot.reply_to(message, response)

# Flask route to keep web service alive
@app.route('/')
def index():
    return "Bot is running!"

# Start polling inside web service
@app.before_first_request
def activate_bot():
    import threading
    threading.Thread(target=bot.polling, kwargs={"none_stop": True}).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
