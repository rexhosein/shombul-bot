import telebot
from telebot import types
import random
import sys
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

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("👑 مهدی ساری", callback_data='mehdi')
    btn2 = types.InlineKeyboardButton("🍬 رادمهر پاستیل", callback_data='radmehr')
    btn3 = types.InlineKeyboardButton("🍑 سهیل همدونی", callback_data='soheil')
    btn4 = types.InlineKeyboardButton("🚩 گزارش جدید", callback_data='report')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", parse_mode="HTML", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    back = types.InlineKeyboardMarkup()
    back.add(types.InlineKeyboardButton("🔙 بازگشت به لیست", callback_data='back'))

    if call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup()
        m_markup.add(types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'))
        m_markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back'))
        cap = f"👤 <b>پرونده: مهدی ساری</b>\n\nتوسط: {BOT_NAME}\nجرم: کونی منطقه ۱۹ 💩\nتوضیحات: این همون مهدیه که نصف شب میاد تو کوچه داد می‌زنه! مراقب باشید."
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", reply_markup=m_markup)
    
    elif call.data == "rate_mehdi":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"📊 نتیجه آنالیز: مهدی ساری {p}% کونیه! 🤐", show_alert=True)

    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup()
        r_markup.add(types.InlineKeyboardButton("🍭 تست درصد پاستیلی بودن", callback_data='rate_radmehr'))
        r_markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back'))
        cap = f"👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوسط: {BOT_NAME}\nتوضیحات: بو پاستیل میده 🍬\nاین رفیقمون از اوناست که پاستیل می‌بینه خودش رو گم می‌کنه!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "rate_radmehr":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"🍬 رادمهر حدود {p}% پاستیله و بوی توت‌فرنگی میده!", show_alert=True)

    elif call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="🍑 ویس سهیل همدونی", reply_markup=back)

    elif call.data == "report":
        msg = bot.send_message(call.message.chat.id, "📝 اسم فرد و جرمش رو بنویس:")
        bot.register_next_step_handler(msg, save_report)

    elif call.data == "back":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, f"مـنوی اصـلی {BOT_NAME}\nیکی رو انتخاب کن:", parse_mode="HTML", reply_markup=main_menu())

    bot.answer_callback_query(call.id)

def save_report(message):
    user = message.from_user
    rep = f"🚩 <b>گزارش جدید!</b>\n👤 فرستنده: {user.first_name}\n📝 متن: {message.text}"
    bot.send_message(ADMIN_ID, rep, parse_mode="HTML")
    bot.reply_to(message, "✅ گزارش شما ارسال شد!")

if __name__ == "__main__":
    print("🚀 در حال راه اندازی...")
    Thread(target=run).start()
    bot.infinity_polling()
