import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# --- تنظیمات سرور برای پایداری ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8000)

# --- تنظیمات اصلی ---
TOKEN = "8543493612:AAHha9_7ph-kaxYCKPpztLQoeFiMygCrsUY"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 1009877033 

# دیتابیس کاربران در حافظه
user_data = {}

def get_stats(user_id):
    if user_id not in user_data:
        user_data[user_id] = {'pastils': 10, 'name': 'ناشناس'}
    return user_data[user_id]

# --- منوی اصلی (شیشه‌ای) ---
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

# --- مدیریت پیام‌های متنی و دکمه‌های ثابت ---
@bot.message_handler(func=lambda m: True)
def text_handler(message):
    uid = message.from_user.id
    if uid == ADMIN_ID and message.text.startswith("set_pastil"):
        try:
            _, target_id, amount = message.text.split()
            get_stats(int(target_id))['pastils'] += int(amount)
            bot.reply_to(message, f"✅ ایول رئیس! حساب {target_id} رو {amount} تا شارژ کردم.")
        except: pass
        return

    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "منوی انتخاب کونی‌ها: 👇", reply_markup=main_menu())
    
    elif message.text == "🚕 اسنپ اوشاخلاری":
        # توضیحات کامل رادین هول
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = (
            "👤 <b>پرونده: رادین هول</b>\n\n"
            "📝 توضیحات: راننده اسنپ بدبو! 💨 جوری بوی جوراب میده که مسافر وسط اتوبان پیاده میشه!\n\n"
            "🚩 <b>لیست اکس‌ها:</b>\n"
            "سلنا، النا، مائده، نسترن، عسل، غزل، مهسا، پریا، سوگند و... (این لیست هر ساعت آپدیت میشه!)\n\n"
            "⚠️ وضعیت: بسیار خطرناک برای دختران محل!"
        )
        bot.send_photo(message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

# --- مدیریت دکمه‌های شیشه‌ای (Callbacks) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    uid = call.from_user.id
    stats = get_stats(uid)
    stats['name'] = call.from_user.first_name

    # 1. پرونده مهدی ساری
    if call.data == 'case_mehdi':
        cap = (
            "👤 <b>پرونده: مهدی ساری</b>\n\n"
            "جرم: کونیِ تراز اول منطقه! 💩\n\n"
            "توضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن! "
            "مراقب ماتحت خود باشید که این بشر رحم نداره."
        )
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # 2. پرونده رادمهر پاستیل
    elif call.data == 'case_radmehr':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("👤 مشاهده رئیس (حسین پاستیل)", callback_data='go_boss'),
                   types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main'))
        cap = (
            "👤 <b>پرونده: رادمهر پاستیل</b>\n\n"
            "توضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬\n"
            "میگن شبا با پاستیل نوشابه‌ای می‌خوابه و صبح‌ها با طعم توت فرنگی بیدار میشه!"
        )
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=markup)

    # 3. سهیل همدونی (ویس سالم و تضمینی)
    elif call.data == 'case_soheil':
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        cap = "👤 <b>پرونده: سهیل همدونی</b>\n\nجرم: اوبنه‌ای تراز اول! 🍑\nتوضیحات: این همون کونی‌ایه که آمار همرو به گا میده!"
        bot.send_voice(call.message.chat.id, v_id, caption=cap, parse_mode="HTML", 
                       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')))

    # 4. پنل بازی و رئیس (حسین)
    elif call.data == 'go_boss':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='check_stats'),
            types.InlineKeyboardButton("🎮 شروع عملیات دزدی", callback_data='game_init'),
            types.InlineKeyboardButton("👑 شاه دزد پاستیل (برترین‌ها)", callback_data='game_rank'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_main')
        )
        cap = "🕶 <b>پنل مدیریت عملیات رئیس حسین</b>\n\nرادمهر (پسرش) جلوی در انبار نگهبانی میده! حواست باشه."
        bot.edit_message_media(media=types.InputMediaPhoto("https://i.ibb.co/27XKnLBd/image.png", caption=cap, parse_mode="HTML"), 
                               chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    # شروع بازی
    elif call.data == 'game_init':
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🍭 رشوه (۲ پاستیل)", callback_data='game_bribe'),
            types.InlineKeyboardButton("👣 مخفیانه رد شو", callback_data='game_sneak')
        )
        bot.edit_message_caption("💂 رادمهر جلو در انبار ایستاده! چیکار می‌کنی کونی؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'game_bribe':
        if stats['pastils'] >= 2:
            stats['pastils'] -= 2
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار و دزدی", callback_data='game_final'))
            bot.edit_message_caption("✅ رادمهر رشوه رو گرفت و رفت! حالا وقتشه بزنی به انبار:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ پاستیل نداری گدا! برو کارگری کن.", show_alert=True)

    elif call.data == 'game_sneak':
        if random.random() < 0.45:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار و دزدی", callback_data='game_final'))
            bot.edit_message_caption("✅ ایول! رادمهر متوجه نشد. سریع برو تو:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            stats['pastils'] = max(0, stats['pastils'] - 5)
            bot.answer_callback_query(call.id, "❌ مچتو گرفتن! رادمهر ۵ تا پاستیل جریمه‌ات کرد.", show_alert=True)
            bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'game_final':
        stolen = random.randint(10, 40)
        if random.random() > 0.35:
            stats['pastils'] += stolen
            bot.answer_callback_query(call.id, f"💎 ایول! {stolen} تا پاستیل دزدیدی و جیم زدی!", show_alert=True)
        else:
            stats['pastils'] = 0
            bot.answer_callback_query(call.id, "❌ حسین بیدار شد! همه‌چیز رو ازت گرفت و یه لگد هم بهت زد! 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "برگشتیم منوی اصلی:", reply_markup=main_menu())

    # لیست برترین‌ها
    elif call.data == 'game_rank':
        top_users = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "👑 <b>لیست شاه دزدان پاستیل محله:</b>\n\n"
        if not top_users: lb += "فعلاً دزدی انجام نشده کونی‌ها!"
        else:
            for i, (uid, data) in enumerate(top_users, 1):
                lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} 🍭\n"
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, parse_mode="HTML", 
                                 reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='go_boss')))

    # بازگشت کلی
    elif call.data == 'back_main':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu())

    elif call.data == 'check_stats':
        bot.answer_callback_query(call.id, f"موجودی شما: {stats['pastils']} پاستیل", show_alert=True)

    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
