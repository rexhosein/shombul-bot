import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات وب‌سرور برای کویِب ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# --- تابع ساخت منوی چسبیده پایین (Reply Keyboard) ---
def permanent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # این خط باعث میشه دکمه‌ها اندازه مناسب بگیرن
    btn_start = types.KeyboardButton("🏠 بازگشت به منوی اصلی")
    markup.add(btn_start)
    return markup

# --- منوی شیشه‌ای اصلی ---
def main_menu_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("👑 مهدی ساری", callback_data='mehdi')
    btn2 = types.InlineKeyboardButton("🍬 رادمهر پاستیل", callback_data='radmehr')
    btn3 = types.InlineKeyboardButton("🍑 سهیل همدونی", callback_data='soheil')
    btn4 = types.InlineKeyboardButton("🚩 گزارش جدید", callback_data='report')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    # اینجا هم منوی شیشه‌ای رو میفرستیم هم منوی چسبیده پایین رو فعال میکنیم
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", 
                     reply_markup=permanent_menu()) # منوی پایین فعال میشه
    
    bot.send_message(message.chat.id, "یکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu_inline())

# --- پاسخ به دکمه چسبیده پایین ---
@bot.message_handler(func=lambda message: message.text == "🏠 بازگشت به منوی اصلی")
def back_to_home(message):
    bot.send_message(message.chat.id, "برگشتیم منوی اصلی! 👇", reply_markup=main_menu_inline())

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    # کدهای قبلی رادمهر و مهدی و غیره اینجا باشن (همون کدهایی که تو مرحله قبل برات فرستادم)
    # ... (بقیه بخش‌های callback_answer رو طبق کد قبلی اینجا قرار بده)
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
