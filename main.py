import os, threading
from flask import Flask
import telebot
from groq import Groq

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)
SYSTEM = "انت Bestie رفيق سوري عامي قصير."

def ask(t):
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":SYSTEM},{"role":"user","content":t}],
            temperature=0.8
        )
        return r.choices[0].message.content
    except Exception as e:
        print(f"GROQ ERROR: {e}")
        return f"صار معي مشكلة تقنية: {e} - ابعت سكرين لخضر"

@bot.message_handler(commands=['start'])
def s(m): bot.send_message(m.chat.id, "هلا أنا Bestie 🌙 شغال 24 ساعة!")

@bot.message_handler(func=lambda m: True)
def a(m):
    bot.send_chat_action(m.chat.id, 'typing')
    reply = ask(m.text)
    bot.send_message(m.chat.id, reply)

app = Flask(__name__)
@app.route('/')
def home(): return "Bestie is alive!"

def run_bot():
    print("BOT STARTED")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))