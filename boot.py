import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای زنده نگه داشتن ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 1009877033 
BOT_NAME = "<b>⚡️ شـومبـول عـلـی ⚡️</b>"

# دیتابیس موقت در حافظه
user_data = {}

def get_user_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'pastils': 10, 'shoes': False, 'spray': False, 'name': 'ناشناس'}
    return user_data[user_id]

# --- منوی اصلی ---
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
    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("🏠 بازگشت به منوی اصلی", "🚕 اسنپ اوشاخلاری"))
    bot.send_message(message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu_inline())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.from_user.id == ADMIN_ID and message.text.startswith("set_pastil"):
        try:
            parts = message.text.split()
            uid = int(parts[1]); amt = int(parts[2])
            u_stats = get_user_stats(uid)
            u_stats['pastils'] += amt
            bot.reply_to(message, f"✅ رئیس! حساب {uid} به مقدار {amt} شارژ شد.")
        except: bot.reply_to(message, "❌ فرمت غلطه رئیس! مثال: set_pastil 123456 100")
        return

    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "لیست اصلی کونی‌ها: 👇", reply_markup=main_menu_inline())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری (همه بدبو):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    user_id = call.from_user.id; stats = get_user_stats(user_id)
    stats['name'] = call.from_user.first_name
    
    # --- 🍑 بخش سهیل همدونی (اصلاح شده) ---
    if call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="👤 <b>پرونده: سهیل همدونی</b>\n\nجرم: اوبنه‌ای تراز اول! 🍑\nتوضیحات: این همون کونی‌ایه که آمار همرو به گا میده!", 
                       parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    # --- 🍭 پنل رئیس حسین و بازی دزدی (اصلاح شده) ---
    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='alert_stats'),
            types.InlineKeyboardButton("🎮 شروع عملیات دزدی", callback_data='game_start'),
            types.InlineKeyboardButton("👑 شاه دزد پاستیل", callback_data='leaderboard_fix'),
            types.InlineKeyboardButton("➕ دریافت پاستیل", callback_data='get_pastil'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr'))
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption=f"🕶 <b>پنل مدیریت عملیات رئیس حسین</b>\n\n💰 موجودی تو: {stats['pastils']} پاستیل\nرادمهر دمِ در انبار نگهبانی میده!", parse_mode="HTML"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=boss_markup)

    elif call.data == "game_start":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🍭 رشوه (۱ پاستیل)", callback_data='game_bribe'), types.InlineKeyboardButton("👣 مخفیانه", callback_data='game_sneak'))
        bot.edit_message_caption("💂 رادمهر جلو انبار ایستاده! چیکار می‌کنی کونی؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "game_bribe":
        if stats['pastils'] >= 1:
            stats['pastils'] -= 1
            bot.edit_message_caption("✅ رادمهر رشوه رو گرفت و رفت پاستیل بخوره! راه باز شد.", call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار حسین", callback_data='game_final')))
        else: bot.answer_callback_query(call.id, "❌ پاستیل نداری گدا!", show_alert=True)

    elif call.data == "game_sneak":
        if random.random() < 0.4:
            bot.edit_message_caption("✅ ایول! رادمهر خواب بود، رد شدی.", call.message.chat.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار", callback_data='game_final')))
        else:
            stats['pastils'] = max(0, stats['pastils'] - 5)
            bot.answer_callback_query(call.id, "❌ مچتو گرفتن! رادمهر ۵ تا پاستیل جریمه‌ات کرد.", show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "game_final":
        stolen = random.randint(5, 30)
        if random.random() > 0.4:
            stats['pastils'] += stolen
            bot.answer_callback_query(call.id, f"💎 ایول! {stolen} تا پاستیل زدی به جیب و فرار کردی!", show_alert=True)
        else:
            stats['pastils'] = 0
            bot.answer_callback_query(call.id, "❌ حسین بیدار شد! همه‌چیز رو ازت گرفت و یه لگد هم بهت زد! 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # --- 👑 لیست شاه دزدها (فیکس شده) ---
    elif call.data == "leaderboard_fix":
        top = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان پاستیل محله:</b>\n\n"
        if not top: lb += "فعلاً دزدی انجام نشده کونی‌ها!"
        else:
            for i, (uid, data) in enumerate(top, 1):
                lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss')))

    # --- 📄 پرونده‌ها با توضیحات کامل ---
    elif call.data == "mehdi":
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption="👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن! مراقب ماتحت خود باشید.", parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'), types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main'))
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption="👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬\nمیگن شبا با پاستیل نوشابه‌ای می‌خوابه!", parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "radin_hole":
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption="👤 <b>پرونده: رادین هول</b>\n\n📝 راننده اسنپ بدبو! 💨\nلیست اکس‌ها: سلنا، النا، مائده، نسترن، عسل، غزل، مهسا و... (لیست همچنان ادامه دارد)", parse_mode="HTML", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu_inline())

    elif call.data == "alert_stats":
        bot.answer_callback_query(call.id, f"موجودی فعلی شما: {stats['pastils']} پاستیل", show_alert=True)

    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
