import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای کویِب ---
app = Flask('')
@app.route('/')
def home(): return "Shombul Ali is Online!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# --- منوی ثابت پایین ---
def permanent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("🏠 بازگشت به منوی اصلی")
    btn_snap = types.KeyboardButton("🚕 اسنپ اوشاخلاری")
    markup.add(btn_start, btn_snap)
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
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", reply_markup=permanent_menu())
    bot.send_message(message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu_inline())

# --- مدیریت دکمه‌های پایین صفحه ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "برگشتیم لیست اصلی: 👇", reply_markup=main_menu_inline())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup()
        snap_markup.add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

# --- مدیریت کلیک دکمه‌ها (Callbacks) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    
    # مهدی ساری
    if call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')
        )
        cap = f"👤 <b>پرونده: مهدی ساری</b>\n\nتوسط: {BOT_NAME}\nجرم: کونی منطقه ۱۹ 💩\nتوضیحات: این همون مهدیه که نصف شب میاد تو کوچه داد می‌زنه! مراقب باشید."
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", reply_markup=m_markup)
    
    elif call.data == "rate_mehdi":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"📊 نتیجه آنالیز: مهدی ساری {p}% کونیه! 🤐", show_alert=True)

    # رادمهر پاستیل
    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("🍭 تست درصد پاستیلی بودن", callback_data='rate_radmehr'),
            types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')
        )
        cap = f"👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوسط: {BOT_NAME}\nتوضیحات: بو پاستیل میده 🍬\nاین رفیقمون از اوناست که پاستیل می‌بینه خودش رو گم می‌کنه!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "rate_radmehr":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"🍬 رادمهر حدود {p}% پاستیله و بوی توت‌فرنگی میده!", show_alert=True)

    # رئیس حسین پاستیل
    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("💉 تست تستسترون ابوی", callback_data='dad_test'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr')
        )
        cap = "🕶 <b>اطلاعات محرمانه: رئیس بزرگ</b>\n\n👤 <b>نام متهم:</b> حسین پاستیل\n⚖️ <b>جرم:</b> پاستیل زیاد خوردن و قاچاق شکر!\n⚠️ <b>توضیحات:</b> ایشون رئیس کل پاستیلی‌های منطقه هستن."
        bot.send_photo(call.message.chat.id, "https://ibb.co/S4QH0SJF", caption=cap, parse_mode="HTML", reply_markup=boss_markup)

    elif call.data == "dad_test":
        p = random.randint(1, 19)
        bot.answer_callback_query(call.id, f"🧪 نتیجه آزمایش ابوی:\nسطح تستسترون: {p}% (بسیار وخیم و زیر حد مجاز) 📉", show_alert=True)

    # سهیل همدونی
    elif call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="🍑 ویس سهیل همدونی", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    # رادین هول
    elif call.data == "radin_hole":
        rd_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💨 سنجش میزان گوزو بودن", callback_data='rate_radin_fart'),
            types.InlineKeyboardButton("🔙 بازگشت به اسنپ", callback_data='back_to_snap_list')
        )
        cap = (f"👤 <b>پرونده: رادین هول</b>\n\n"
               f"📝 <b>توضیحات:</b> راننده بدبو و از خوبای اسنپ اوشاخلاری! 💨\n\n"
               f"💖 <b>لیست Exها:</b>\n❌ سلنا، النا، سیما، شیما، فاطی و ...\n\n"
               f"⚠️ <b>هشدار:</b> خطر نشت گاز، فندک نزنید!")
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=rd_markup)

    elif call.data == "rate_radin_fart":
        p = random.randint(71, 100)
        bot.answer_callback_query(call.id, f"⚠️ هشدار آلودگی:\nمیزان گوزو بودن رادین {p}% است! (وضعیت قرمز) 😷", show_alert=True)

    # دکمه‌های بازگشت
    elif call.data == "back_to_main":
        bot.

