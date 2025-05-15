import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

CHARACTER = "You are a sensual, poetic fantasy elf princess. Speak gently and romantically with immersive roleplay."

def ask_ai(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gryphe/mythy-7b",
        "messages": [
            {"role": "system", "content": CHARACTER},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "AI এর সাথে সংযোগ ব্যর্থ হয়েছে। পরে আবার চেষ্টা করুন।"

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, "স্বাগতম! Fantasy chat করতে এখন সরাসরি বার্তা পাঠান।")

@bot.message_handler(func=lambda m: True)
def chat(msg):
    user_text = msg.text
    bot.send_chat_action(msg.chat.id, 'typing')
    ai_reply = ask_ai(user_text)
    bot.reply_to(msg, ai_reply)

@app.route('/')
def index():
    return "Bot is Running!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://chatbot-s8g6.onrender.com/{BOT_TOKEN}")  # তোমার URL এখানে সঠিক বসাও
    app.run(host="0.0.0.0", port=10000)
