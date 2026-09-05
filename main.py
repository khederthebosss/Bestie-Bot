import os
import telebot
from groq import Groq
import traceback

# بياخد المفاتيح من Render مشان ما ينسرقو
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

if not BOT_TOKEN or not GROQ_KEY:
    print("حط BOT_TOKEN و GROQ_KEY بـ Environment Variables بـ Render!")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

SYSTEM = "انت Bestie رفيق سوري بتحكي عامي شامي قصير ومهضوم. اذا حدا سألك شي طبي قل بدو دكتور مختص."

def ask(text):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":text}]
    )
    return r.choices[0].message.content

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "هلا أنا Bestie 🌙\nرفيقك اللي بيسمعك بلا ملل\n\nاحكيلي شو مضايقك اليوم؟")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        ans = ask(m.text)
        bot.send_message(m.chat.id, ans)
    except Exception as e:
        print(traceback.format_exc())
        bot.send_message(m.chat.id, "دقيقة علق مخي، جرب مرة تانية 😅")

print("Bestie شغال...")
bot.infinity_polling()