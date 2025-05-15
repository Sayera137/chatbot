import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

CHARACTER = "তুমি একজন কামুক এলফ রাজকুমারী। তোমার কণ্ঠ কোমল, প্রেমময় ও রোমান্টিক।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! Fantasy chat করতে /chat লিখুন।")

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    user_input = message.text.replace("/chat", "").strip()
    if not user_input:
        bot.reply_to(message, "দয়া করে /chat এর পর কিছু লিখুন।")
        return

    prompt = f"{CHARACTER}\nUser: {user_input}\nAI:"
    response = call_openrouter_api(prompt)

    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "AI থেকে উত্তর পাওয়া যায়নি।")

def call_openrouter_api(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openrouter/pygmalion-2.7b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.95
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("API error:", e)
        return None

print("Bot is running...")
bot.remove_webhook()
bot.polling()
