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
    if len(message.text.split()) > 1 and message.text.split()[1].startswith('ref_'):
        ref_id = int(message.text.split()[1].replace('ref_', ''))
        if ref_id != user_id and 'invited_by' not in stats:
            ref_stats = get_user_stats(ref_id)
            ref_stats['pastils'] += 50
            stats['invited_by'] = ref_id
            bot.send_message(ref_id, f"🎊 تبریک! یک نفر با لینک تو اومد و ۵۰ پاستیل گرفتی!")
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
            bot.reply_to(message, f"✅ حساب {target_id} شارژ شد.")
            bot.send_message(target_id, f"💎 حسابت {amount} پاستیل توسط ادمین شارژ شد!")
        except: bot.reply_to(message, "❌ غلطه! مثال: set_pastil ID Amount")
        return
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "لیست اصلی کونی‌ها: 👇", reply_markup=main_menu_inline())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    user_id = call.from_user.id; stats = get_user_stats(user_id)
    stats['name'] = call.from_user.first_name
    
    if call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='show_stats_alert'),
            types.InlineKeyboardButton("🎮 شروع عملیات دزدی", callback_data='game_step1'),
            types.InlineKeyboardButton("👑 شاه دزد پاستیل", callback_data='leaderboard'),
            types.InlineKeyboardButton("🛒 فروشگاه تجهیزات", callback_data='game_shop'),
            types.InlineKeyboardButton("➕ دریافت پاستیل (خرید/دعوت)", callback_data='get_pastil_list'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr'))
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption=f"🕶 <b>پنل مدیریت عملیات رئیس حسین</b>\n\n💰 موجودی تو: {stats['pastils']} پاستیل", parse_mode="HTML"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=boss_markup)

    elif call.data == "leaderboard":
        top_users = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان پاستیل محله:</b>\n\n"
        for i, (uid, data) in enumerate(top_users, 1): lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss')), parse_mode="HTML")

    elif call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption="👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن!", parse_mode="HTML", reply_markup=m_markup)

    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🍭 تست پاستیلی بودن", callback_data='rate_radmehr'), types.InlineKeyboardButton("👤 مشاهده رئیس", callback_data='radmehr_boss'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption="👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬", parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "get_pastil_list":
        markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🤝 دعوت (۵۰ پاستیل)", callback_data='invite_friends'), types.InlineKeyboardButton("💳 خرید پکیج", callback_data='buy_money'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss'))
        bot.edit_message_caption("📜 روش‌های کسب پاستیل:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "buy_money":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📸 ارسال رسید به ربات", callback_data='send_receipt_to_bot'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='get_pastil_list'))
        bot.edit_message_caption("💳 <b>شماره کارت:</b>\n<code>6219-8619-1556-6334</code>\nبنام: لیلا حسن پور فرخی", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "send_receipt_to_bot":
        msg = bot.send_message(call.message.chat.id, "📥 عکس رسید رو بفرست:")
        bot.register_next_step_handler(msg, process_receipt)

    elif call.data == "game_step1":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🍭 رشوه (۱ پاستیل)", callback_data='bribe'), types.InlineKeyboardButton("👣 مخفیانه", callback_data='sneak'))
        bot.edit_message_caption("💂 رادمهر نگهبانه! چیکار می‌کنی؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی اصلی:", reply_markup=main_menu_inline())

    bot.answer_callback_query(call.id)

def process_receipt(message):
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"🚩 رسید جدید!\n🆔 آیدی: <code>{message.from_user.id}</code>\n✅ دستور شارژ:\n<code>set_pastil {message.from_user.id} 100</code>", parse_mode="HTML")
        bot.reply_to(message, "✅ رسید فرستاده شد.")
    else: bot.reply_to(message, "❌ فقط عکس بفرست.")

def save_report(message):
    bot.send_message(ADMIN_ID, f"🚩 گزارش جدید:\n👤 از: {message.from_user.first_name}\n📝 متن: {message.text}")
    bot.reply_to(message, "✅ حله، شومبول علی ردیفش می‌کنه!")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
