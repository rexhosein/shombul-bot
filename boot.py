import telebot
import os
from flask import Flask
from threading import Thread

# --- بخش جدید برای گول زدن کویِب ---
app = Flask('')
@app.route('/')
def home():
    return "بیا، پورت بازه! دست از سر ربات بردار."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------

bot = telebot.TeleBot("توکن_خودت_رو_اینجا_بذار")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ شومبول علی روی سرور ابری زنده شد!")

if __name__ == "__main__":
    keep_alive() # روشن کردن سرور الکی
    print("✅ ربات بدون هیچ باگی آماده استفاده است")
    bot.infinity_polling()
