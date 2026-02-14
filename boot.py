import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای زنده نگه داشتن ربات ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 1009877033 

user_data = {}

def get_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'pastils': 15, 'name': 'ناشناس'}
    return user_data[user_id]

# --- منوی اصلی ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👑 مهدی ساری", callback_data='case_mehdi'),
        types.InlineKeyboardButton("🍬 رادمهر پاستیل", callback_data='case_radmehr'),
        types.InlineKeyboardButton("🍑 سهیل همدونی", callback_data='case_soheil'),
        types.InlineKeyboardButton("🚩 گزارش جدید", callback_data='case_report')
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    get_stats(uid)['name'] = message.from_user.first_name
    bot.send_message(message.chat.id, "سـلام! مـن <b>⚡️ شـومبـول عـلـی ⚡️</b> هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("🏠 بازگشت به منوی اصلی", "🚕 اسنپ اوشاخلاری"))
    bot.send_message(message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def text_handler(message):
    uid = message.from_user.id
    if uid == ADMIN_ID and message.text.startswith("set_pastil"):
        try:
            _, target_id, amount = message.text.split()
            get_stats(int(target_id))['pastils'] += int(amount)
            bot.reply_to(message, f"✅ انجام شد رئیس! حساب {target_id} شارژ شد.")
        except: pass
        return

    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "منوی انتخاب کونی‌ها: 👇", reply_markup=main_menu())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = (
            "👤 <b>پرونده: رادین هول</b>\n\n"
            "📝 توضیحات: راننده اسنپ بدبو! 💨 جوری بوی جوراب میده که مسافر غش می‌کنه!\n"
            "🚩 <b>لیست اکس‌ها:</b> سلنا، النا، مائده، نسترن، عسل، غزل، مهسا و..."
        )
        bot.send_photo(message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    uid = call.from_user.id
    stats = get_stats(uid)
    stats['name'] = call.from_user.first_name

    # جلوگیری از باگ نمایش عکس
    if call.data in ['case_mehdi', 'case_radmehr', 'case_soheil']:
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass

    # 1. پرونده مهدی ساری
    if call.data == 'case_mehdi':
        cap = "👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # 2. پرونده رادمهر پاستیل
    elif call.data == 'case_radmehr':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("👤 ورود به پنل رئیس (حسین پاستیل)", callback_data='go_boss'),
                   types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = "👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

    # 3. پرونده سهیل همدونی
    elif call.data == 'case_soheil':
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="👤 <b>سهیل همدونی</b>\nجرم: اوبنه‌ای تراز اول! 🍑", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # 4. پنل مدیریت بازی
    elif call.data == 'go_boss':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='n'),
            types.InlineKeyboardButton("🎮 دستبرد به انبار حسین پاستیل", callback_data='g_start'),
            types.InlineKeyboardButton("👑 لیست شاه‌دزدان (برترین‌ها)", callback_data='g_rank'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')
        )
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption="🕶 <b>پنل مخفی رئیس حسین</b>\nرادمهر نگهبانی میده، حواستو جمع کن!"), 
                               chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    # --- شروع بازی دزدی ---
    elif call.data == 'g_start':
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🍭 رشوه (۳ پاستیل)", callback_data='g_bribe'),
            types.InlineKeyboardButton("👣 مخفیانه رد شو", callback_data='g_sneak')
        )
        bot.edit_message_caption("💂 رادمهر جلو در انبار ایستاده! چیکار می‌کنی کونی؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'g_bribe':
        if stats['pastils'] >= 3:
            stats['pastils'] -= 3
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار و دزدی", callback_data='g_final'))
            bot.edit_message_caption("✅ رادمهر رشوه رو گرفت. سریع برو تو انبار:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ پاستیل نداری گدا!", show_alert=True)

    elif call.data == 'g_sneak':
        if random.random() < 0.4:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار", callback_data='g_final'))
            bot.edit_message_caption("✅ ایول! رادمهر نفهمید. سریع برو تو:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            stats['pastils'] = max(0, stats['pastils'] - 5)
            bot.answer_callback_query(call.id, "❌ مچتو گرفتن! ۵ تا پاستیل جریمه شدی! 😂", show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "شکست خوردی! دوباره تلاش کن:", reply_markup=main_menu())

    elif call.data == 'g_final':
        win = random.randint(15, 45)
        if random.random() > 0.4:
            stats['pastils'] += win
            bot.answer_callback_query(call.id, f"💎 ایول! {win} تا پاستیل دزدیدی!", show_alert=True)
        else:
            stats['pastils'] = 0
            bot.answer_callback_query(call.id, "❌ حسین بیدار شد و همشو ازت گرفت! 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "عملیات تموم شد. منوی اصلی:", reply_markup=main_menu())

    # --- بخش شاه‌دزد (Leaderboard) ---
    elif call.data == 'g_rank':
        top_users = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان پاستیل محله:</b>\n\n"
        if not top_users:
            lb += "هنوز کسی دزدی نکرده کونی‌ها!"
        else:
            for i, (uid, data) in enumerate(top_users, 1):
                lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, parse_mode="HTML", 
                                 reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='go_boss')))

    # بازگشت کلی
    elif call.data == 'back_main':
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu())

    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
