import os
import threading 
from flask import Flask
import telebot
from groq import Groq
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY") or os.getenv("GROQ_KEY")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "KhederMhd")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

SYSTEM = "انت اسمك Bestie. رفيق شخصي بتحكي عامي سوري خفيف، قصير ومهضوم."

def ask(text):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":text}]
    )
    return r.choices[0].message.content

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "هلا أنا Bestie 🌙\nرفيقك اللي بيسمعك دائما.")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    try:
        ans = ask(m.text)
        bot.send_message(m.chat.id, ans)
    except Exception as e:
        print(f"ERROR: {e}")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📩 تواصل مع خضر", url=f"https://t.me/{SUPPORT_USERNAME}"))
        bot.send_message(m.chat.id,
            "⚠️ **عذراً، حدث خلل فني مؤقت**\n\n"
            "ما قدرت أعالج طلبك هلأ بسبب ضغط على النظام.\n"
            "جرب ترجع بعد دقيقة، واذا بقيت المشكلة فريقنا جاهز يساعدك.\n\n"
            "اضغط الزر تحت للتواصل المباشر 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )

print("Bestie شغال...")
bot.infinity_polling()