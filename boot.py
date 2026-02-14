import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات وب‌سرور برای کویِب ---
app = Flask('')
@app.route('/')
def home(): return "Shombul Ali is Online!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# --- منوی چسبیده پایین (ثابت) ---
def permanent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # اضافه کردن دو دکمه در یک ردیف (بغل هم)
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

# --- مدیریت پیام‌های متنی (دکمه‌های پایین) ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "برگشتیم لیست اصلی: 👇", reply_markup=main_menu_inline())
    
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup()
        snap_markup.add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

# --- مدیریت کلیک روی دکمه‌های شیشه‌ای ---
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    back_main = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت به لیست اصلی", callback_data='back'))

    # --- مهدی ساری ---
    if call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back')
        )
        cap = f"👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونی منطقه ۱۹ 💩\nتوضیحات: این همون مهدیه که نصف شب میاد تو کوچه داد می‌زنه!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", reply_markup=m_markup)
    
    elif call.data == "rate_mehdi":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"📊 نتیجه آنالیز: مهدی ساری {p}% کونیه! 🤐", show_alert=True)

    # --- رادمهر پاستیل و رئیس ---
    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("🍭 تست پاستیلی بودن", callback_data='rate_radmehr'),
            types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back')
        )
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption="👤 <b>پرونده: رادمهر پاستیل</b>\nمعامله‌گر پاستیل‌های غیرمجاز! 🍬", parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("💉 تست تستسترون ابوی", callback_data='dad_test'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr')
        )
        cap = "🕶 <b>رئیس بزرگ: حسین پاستیل</b>\n⚖️ <b>جرم:</b> پاستیل‌خواری مفرط!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=boss_markup)

    elif call.data == "dad_test":
        p = random.randint(1, 19)
        bot.answer_callback_query(call.id, f"🧪 نتیجه آزمایش ابوی:\nسطح تستسترون: {p}% (وضعیت وخیم) 📉", show_alert=True)

    # --- سهیل همدونی ---
    elif call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="🍑 ویس سهیل همدونی", reply_markup=back_main)

    # --- رادین هول ---
    elif call.data == "radin_hole":
        rd_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💨 سنجش گوزو بودن", callback_data='rate_radin_fart'),
            types.InlineKeyboardButton("🔙 بازگشت به اسنپ", callback_data='back_to_snap')
        )
        cap = (f"👤 <b>پرونده: رادین هول</b>\n\n📝 <b>توضیحات:</b> راننده بدبو! 💨\n"
               f"❌ <b>لیست Exها:</b> سلنا، النا، سیما، شیما، فاطی...\n⚠️ فندک نزنید!")
        # جای این لینک پایین، لینک عکس رادین رو بذار
        bot.send_photo(call.message.chat.id, "https://ibb.co/sDKtLP5", caption=cap, parse_mode="HTML", reply_markup=rd_markup)

    elif call.data == "rate_radin_fart":
        p = random.randint(71, 100)
        bot.answer_callback_query(call.id, f"⚠️ هشدار:\nمیزان گوزو بودن رادین {p}% است! 😷", show_alert=True)

    elif call.data == "back_to_snap":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        snap_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(call.message.chat.id, "🚕 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی انتخاب:", reply_markup=main_menu_inline())

    elif call.data == "report":
        msg = bot.send_message(call.message.chat.id, "📝 اسم فرد و جرمش رو بنویس:")
        bot.register_next_step_handler(msg, save_report)

    bot.answer_callback_query(call.id)

def save_report(message):
    bot.send_message(ADMIN_ID, f"🚩 گزارش: {message.text}")
    bot.reply_to(message, "✅ ارسال شد!")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
