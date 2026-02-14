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
        cap = f"👤 <b>پرونده: مهدی ساری</b>\n\nتوسط: {BOT_NAME}\nجرم: کونی منطقه ۱۹ 💩\nتوضیحات: این همون مهدیه که نصف شب میاد تو کوچه داد می‌زنه!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", reply_markup=m_markup)
    
    elif call.data == "rate_mehdi":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"📊 نتیجه آنالیز: مهدی ساری {p}% کونیه! 🤐", show_alert=True)

    # --- بخش جدید رادمهر ---
    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1)
        r_markup.add(
            types.InlineKeyboardButton("🍭 تست درصد پاستیلی بودن", callback_data='rate_radmehr'),
            types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back')
        )
        cap = f"👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوسط: {BOT_NAME}\nتوضیحات: نامبرده به دلیل معامله پاستیل‌های غیرمجاز تحت نظر است! 🍬"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup()
        boss_markup.add(types.InlineKeyboardButton("💉 تست تستسترون ابوی (پدر)", callback_data='dad_test'))
        boss_markup.add(types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr'))
        cap = "🕶 <b>اطلاعات محرمانه: رئیس بزرگ</b>\n\n👤 <b>نام متهم:</b> حسین پاستیل\n⚖️ <b>جرم:</b> پاستیل زیاد خوردن و قاچاق شکر!\n⚠️ <b>وضعیت:</b> به شدت پاستیلی!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=boss_markup)

    elif call.data == "dad_test":
        p = random.randint(1, 19) # تست زیر 20 درصد
        bot.answer_callback_query(call.id, f"🧪 نتیجه آزمایش ابوی:\nسطح تستسترون: {p}% (بسیار پایین و وخیم) 📉", show_alert=True)

    elif call.data == "rate_radmehr":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"🍬 رادمهر حدود {p}% پاستیله!", show_alert=True)

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
    Thread(target=run).start()
    bot.infinity_polling()
