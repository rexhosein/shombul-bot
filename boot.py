import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات وب‌سرور برای زنده ماندن در کویِب ---
app = Flask('')
@app.route('/')
def home(): return "Shombul Ali is Alive!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# --- منوی چسبیده پایین صفحه (Reply Keyboard) ---
def permanent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("🏠 بازگشت به منوی اصلی")
    btn_snap = types.KeyboardButton("🚕 اسنپ اوشاخلاری")
    markup.add(btn_start, btn_snap)
    return markup

# --- منوی شیشه‌ای لیست اصلی ---
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
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", reply_markup=permanent_menu())
    bot.send_message(message.chat.id, "لیست نفرات اصلی:", reply_markup=main_menu_inline())

# --- مدیریت دکمه‌های متنی پایین ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "برگشتیم لیست اصلی: 👇", reply_markup=main_menu_inline())
    
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup()
        snap_markup.add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

# --- مدیریت تمام کلیک‌های دکمه‌های شیشه‌ای ---
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    back = types.InlineKeyboardMarkup()
    back.add(types.InlineKeyboardButton("🔙 بازگشت به لیست اصلی", callback_data='back'))

    # --- پرونده مهدی ساری ---
    if call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup()
        m_markup.add(types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'))
        m_markup.add(types.Inline
