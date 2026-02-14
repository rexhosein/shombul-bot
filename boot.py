import telebot
from flask import Flask
from threading import Thread

# تنظیمات وب‌سرور برای کویِب
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run(): app.run(host='0.0.0.0', port=8000)

# توکن رو اینجا بین دو کوتیشن بذار
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "سلام حسین! من الان بیدارم و کار می‌کنم. 🚀")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
