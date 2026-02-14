8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUYimport telebot
import os
from flask import Flask
from threading import Thread

# تنظیمات سرور داخلی برای گول زدن کویِب
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- توکن خودت رو بین دو کوتیشن بذار ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY" 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ شومبول علی با موفقیت روی سرور جدید مستقر شد!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"شما گفتی: {message.text}")

if __name__ == "__main__":
    print("🚀 در حال راه اندازی سرور داخلی...")
    keep_alive()
    print("✅ ربات آماده استفاده است...")
    bot.infinity_polling()


