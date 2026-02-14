import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای کویِب ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# دیتابیس موقت
user_data = {}

def get_user_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'pastils': 5, 'shoes': False, 'spray': False, 'name': 'کاربر جدید'}
    return user_data[user_id]

def permanent_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("🏠 بازگشت به منوی اصلی")
    btn_snap = types.KeyboardButton("🚕 اسنپ اوشاخلاری")
    markup.add(btn_start, btn_snap)
    return markup

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
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    stats['name'] = message.from_user.first_name
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", parse_mode="HTML", reply_markup=permanent_menu())
    bot.send_message(message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu_inline())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.from_user.id == ADMIN_ID and message.text.startswith("set_pastil"):
        try:
            parts = message.text.split()
            target_id = int(parts[1]); amount = int(parts[2])
            u_stats = get_user_stats(target_id)
            u_stats['pastils'] += amount
            bot.reply_to(message, f"✅ ایول رئیس! حساب {target_id} رو {amount} تا شارژ کردم.")
            bot.send_message(target_id, f"💎 کونیِ خوش‌شانس! ادمین حسابتو {amount} پاستیل شارژ کرد.")
        except: bot.reply_to(message, "❌ اشتباه نوشتی! مثال:\nset_pastil 123456 500")
        return
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "برگشتیم لیست اصلی کونی‌ها: 👇", reply_markup=main_menu_inline())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری (همه بدبو):", reply_markup=snap_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    user_id = call.from_user.id; stats = get_user_stats(user_id)
    stats['name'] = call.from_user.first_name
    
    # --- پنل رئیس حسین ---
    if call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='show_stats_alert'),
            types.InlineKeyboardButton("🎮 شروع عملیated دزدی", callback_data='game_step1'),
            types.InlineKeyboardButton("👑 شاه دزد پاستیل (برترین‌ها)", callback_data='leaderboard_list'),
            types.InlineKeyboardButton("🛒 فروشگاه تجهیزات", callback_data='game_shop'),
            types.InlineKeyboardButton("➕ دریافت پاستیل (خرید/دعوت)", callback_data='get_pastil_list'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr'))
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption=f"🕶 <b>پنل مدیریت عملیات رئیس حسین</b>\n\n💰 موجودی تو: {stats['pastils']} پاستیل\nرادمهر (پسرش) جلوی در انبار نگهبانی میده!", parse_mode="HTML"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=boss_markup)

    # --- لیست شاه دزدها ---
    elif call.data == "leaderboard_list":
        top_users = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان پاستیل محله:</b>\n\n"
        if not top_users:
            lb += "هنوز کسی دزدی نکرده کونی‌ها! 💩"
        else:
            for i, (uid, data) in enumerate(top_users, 1):
                lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss')), parse_mode="HTML")

    # --- پرونده مهدی ساری ---
    elif call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption="👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن! مراقب ماتحت خود باشید.", parse_mode="HTML", reply_markup=m_markup)

    # --- پرونده رادمهر پاستیل ---
    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🍭 تست پاستیلی بودن", callback_data='rate_radmehr'), types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption="👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬\nمیگن شبا با پاستیل نوشابه ای می‌خوابه!", parse_mode="HTML", reply_markup=r_markup)

    # --- پرونده رادین هول ---
    elif call.data == "radin_hole":
        rd_markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("💨 سنجش گوزو بودن", callback_data='rate_radin_fart'), types.InlineKeyboardButton("🔙 بازگشت به اسنپ", callback_data='back_to_snap_list'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption="👤 <b>پرونده: رادین هول</b>\n\n📝 راننده اسنپ بدبو! 💨\nلیست اکس‌ها: سلنا، النا، مائده، نسترن، عسل، غزل و... (ادامه دارد)", parse_mode="HTML", reply_markup=rd_markup)

    # --- کسب پاستیل و خرید ---
    elif call.data == "get_pastil_list":
        markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🤝 دعوت (۵۰ پاستیل)", callback_data='invite_friends'), types.InlineKeyboardButton("💳 خرید پکیج پاستیل", callback_data='buy_money'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss'))
        bot.edit_message_caption("📜 <b>لیست روش‌های کسب پاستیل:</b>\n\n1️⃣ دعوت از دوستان\n2️⃣ خرید پکیج‌های پاستیل\n3️⃣ کارگری در اسنپ", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "buy_money":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📸 ارسال رسید به ربات", callback_data='send_receipt_to_bot'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='get_pastil_list'))
        bot.edit_message_caption("💎 <b>بسته‌های پاستیل:</b>\n\n🔸 ۱۰۰ پاستیل: ۱۰ هزار تومان\n🔸 ۵۰۰ پاستیل: ۴۰ هزار تومان\n\n💳 <b>شماره کارت:</b>\n<code>6219-8619-1556-6334</code>\nبنام: لیلا حسن پور فرخی", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "send_receipt_to_bot":
        msg = bot.send_message(call.message.chat.id, "📥 لطفاً همین الان <b>عکس رسید</b> رو بفرست:")
        bot.register_next_step_handler(msg, process_receipt)

    elif call.data == "game_step1":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🍭 رشوه (۱ پاستیل)", callback_data='bribe'), types.InlineKeyboardButton("👣 مخفیانه رد شو", callback_data='sneak'))
        bot.edit_message_caption("💂 <b>رادمهر جلو در انبار ایستاده!</b>\nچیکار می‌کنی کونی؟", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی اصلی انتخاب کونی‌ها:", reply_markup=main_menu_inline())

    bot.answer_callback_query(call.id)

def process_receipt(message):
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"🚩 <b>رسید جدید پرداخت!</b>\n\n👤 فرستنده: {message.from_user.first_name}\n🆔 آیدی: <code>{message.from_user.id}</code>\n\n✅ برای شارژ کپی کن:\n<code>set_pastil {message.from_user.id} 100</code>", parse_mode="HTML")
        bot.reply_to(message, "✅ رسیدت دریافت شد. صبر کن تا تایید بشه.")
    else: bot.reply_to(message, "❌ مگه نمیگم فقط عکس رسید بفرست کونی؟ دوباره تلاش کن.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
