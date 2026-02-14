import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ربات ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 1009877033 

user_data = {}

def get_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'pastils': 15, 'name': 'ناشناس'}
    return user_data[user_id]

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
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "منوی انتخاب کونی‌ها: 👇", reply_markup=main_menu())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        # رادین هول با توضیحات کامل
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = (
            "👤 <b>پرونده: رادین هول</b>\n\n"
            "📝 توضیحات: راننده اسنپ بدبو! 💨\n"
            "🚩 <b>لیست اکس‌ها:</b> سلنا، النا، مائده، نسترن، عسل، غزل، مهسا و..."
        )
        bot.send_photo(message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    uid = call.from_user.id
    stats = get_stats(uid)

    # رفع مشکل بالا نیامدن عکس‌ها (پاک کردن متن قبلی)
    if call.data in ['case_mehdi', 'case_radmehr', 'case_soheil']:
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass

    # 1. پرونده مهدی ساری
    if call.data == 'case_mehdi':
        cap = "👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # 2. پرونده رادمهر پاستیل (اصلاح شده)
    elif call.data == 'case_radmehr':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("👤 ورود به پنل رئیس (حسین پاستیل)", callback_data='go_boss'),
                   types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = "👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

    # 3. سهیل همدونی
    elif call.data == 'case_soheil':
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="👤 <b>سهیل همدونی</b>\nجرم: اوبنه‌ای تراز اول! 🍑", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # شروع جایگذاری از اینجا
    elif call.data == 'go_boss':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"💰 جیبِ فعلی: {stats['pastils']} پاستیل", callback_data='none'),
            types.InlineKeyboardButton("🎮 دستبرد به انبار حسین پاستیل", callback_data='g_start'),
            types.InlineKeyboardButton("👑 تالار افتخارات (شاه‌دزدها)", callback_data='g_rank'),
            types.InlineKeyboardButton("🔙 بازگشت به عقب", callback_data='back_main')
        )
        cap = (
            "🕶 <b>به مخفی‌گاه رئیس حسین خوش اومدی!</b>\n\n"
            "پسرش رادمهر جوری دم در کشیک میده که پشه هم رد شه می‌فهمه! "
            "باید یا سبیلشو چرب کنی یا مثل سایه از بغلش رد شی. کدوم کاره‌ای؟"
        )
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption=cap, parse_mode="HTML"), 
                               chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == 'g_start':
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🍭 رشوه لاتی (۳ پاستیل)", callback_data='g_bribe'),
            types.InlineKeyboardButton("👣 شانس خری (مخفیانه)", callback_data='g_sneak')
        )
        bot.edit_message_caption("💂 <b>رادمهر جلو در داره پاستیل خرسی می‌جویه!</b>\nنقشه‌ات چیه کونی؟", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == 'g_bribe':
        if stats['pastils'] >= 3:
            stats['pastils'] -= 3
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 حمله به گاوصندوق حسین", callback_data='g_final'))
            bot.edit_message_caption("✅ <b>ایول!</b> رادمهر تا پاستیل‌ها رو دید چشاش چهارتا شد و راه رو باز کرد. سریع برو تو تا حسین بیدار نشده!", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
        else:
            bot.answer_callback_query(call.id, "❌ جیبت خالیه! پاستیل نداری رشوه بدی کونی.", show_alert=True)

    elif call.data == 'g_sneak':
        if random.random() < 0.35: 
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💰 غارت انبار", callback_data='g_final'))
            bot.edit_message_caption("✅ <b>ایول!</b> مثل گربه رد شدی و رادمهر نفهمید. انبار روبرویته، بزن تو گوشش!", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
        else:
            stats['pastils'] = max(0, stats['pastils'] - 7)
            bot.answer_callback_query(call.id, "❌ رادمهر بوی عطرتو فهمید! مچتو گرفت و ۷ تا پاستیل ازت تیغ زد! 😂", show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "دوباره از منو تلاش کن:", reply_markup=main_menu())

    elif call.data == 'g_final':
        win = random.randint(15, 50) 
        if random.random() > 0.45:
            stats['pastils'] += win
            bot.answer_callback_query(call.id, f"💎 ایووول! {win} تا پاستیل زدی به جیب و قبل از اینکه حسین با چوب بیاد جیم زدی!", show_alert=True)
        else:
            stats['pastils'] = 0
            bot.answer_callback_query(call.id, "❌ ای دل غافل! حسین بیدار شد و جوری با لنگه کفش زد تو سرت که کل پاستیلاتو ریختی و فرار کردی! 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "عملیات تموم شد. بقیه کونی‌ها رو چک کن:", reply_markup=main_menu())
    # پایان جایگذاری

    elif call.data == 'g_final':
        win = random.randint(10, 35)
        if random.random() > 0.4:
            stats['pastils'] += win
            bot.answer_callback_query(call.id, f"💎 ایول! {win} تا پاستیل دزدیدی!", show_alert=True)
        else:
            stats['pastils'] = 0
            bot.answer_callback_query(call.id, "❌ حسین بیدار شد! همشو ازت گرفت! 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "عملیات تموم شد. منوی اصلی:", reply_markup=main_menu())

    elif call.data == 'g_rank':
        top = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان:</b>\n\n"
        for i, (uid, data) in enumerate(top, 1):
            lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, parse_mode="HTML", 
                                 reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='go_boss')))

    elif call.data == 'back_main':
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu())

    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
