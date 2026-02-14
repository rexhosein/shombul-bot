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

# --- دیتابیس موقت کاربران ---
user_data = {}

def get_user_stats(user_id):
    if user_id not in user_data:
        # ۵ پاستیل هدیه برای شروع به همه
        user_data[user_id] = {'pastils': 5, 'shoes': False, 'spray': False, 'name': 'کاربر جدید'}
    return user_data[user_id]

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
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    stats['name'] = message.from_user.first_name

    # چک کردن لینک دعوت
    if len(message.text.split()) > 1 and message.text.split()[1].startswith('ref_'):
        ref_id = int(message.text.split()[1].replace('ref_', ''))
        if ref_id != user_id and 'invited_by' not in stats:
            ref_stats = get_user_stats(ref_id)
            ref_stats['pastils'] += 50
            stats['invited_by'] = ref_id
            bot.send_message(ref_id, f"🎊 تبریک! یک نفر با لینک تو اومد و ۵۰ پاستیل گرفتی!")

    bot.send_message(message.chat.id, f"سـلام! مـن {BOT_NAME} هستـم 😎\nآمار کونی‌های محل رو از من بگیر: 👇", 
                     parse_mode="HTML", reply_markup=permanent_menu())
    bot.send_message(message.chat.id, "یکی رو انتخاب کن:", reply_markup=main_menu_inline())

# --- مدیریت دکمه‌های ثابت پایین ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "🏠 بازگشت به منوی اصلی":
        bot.send_message(message.chat.id, "برگشتیم لیست اصلی کونی‌ها: 👇", reply_markup=main_menu_inline())
    elif message.text == "🚕 اسنپ اوشاخلاری":
        snap_markup = types.InlineKeyboardMarkup()
        snap_markup.add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(message.chat.id, "🚖 لیست رانندگان اسنپ اوشاخلاری (همه بدبو):", reply_markup=snap_markup)

# --- مدیریت کلیک دکمه‌ها (Callbacks) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    user_id = call.from_user.id
    stats = get_user_stats(user_id)
    stats['name'] = call.from_user.first_name
    
    # مهدی ساری
    if call.data == "mehdi":
        m_markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🔥 سنجش میزان کونی بودن", callback_data='rate_mehdi'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')
        )
        cap = f"👤 <b>پرونده: مهدی ساری</b>\n\nجرم: کونیِ تراز اول منطقه! 💩\nتوضیحات: نامبرده نصف شب‌ها تو کوچه جوری نعره می‌زنه که انگار دارن بهش حال میدن! مراقب ماتحت خود باشید."
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/RGHbcmx6/image.png", caption=cap, parse_mode="HTML", reply_markup=m_markup)
    
    elif call.data == "rate_mehdi":
        p = random.randint(85, 100)
        bot.answer_callback_query(call.id, f"📊 واویلا!\nمهدی ساری {p}% کونیه! از دست رفته دیگه! 🤐", show_alert=True)

    # رادمهر پاستیل
    elif call.data == "radmehr":
        r_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("🍭 تست درصد پاستیلی بودن", callback_data='rate_radmehr'),
            types.InlineKeyboardButton("👤 مشاهده رئیس (ارباب پاستیل‌ها)", callback_data='radmehr_boss'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')
        )
        cap = f"👤 <b>پرونده: رادمهر پاستیل</b>\n\nتوضیحات: این بچه جوری بوی پاستیل خرسی میده که مگس‌ها ولش نمی‌کنن! 🍬\nمیگن شبا با پاستیل نوشابه ای می‌خوابه!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/ZprsGm1t/image.png", caption=cap, parse_mode="HTML", reply_markup=r_markup)

    elif call.data == "rate_radmehr":
        p = random.randint(81, 100)
        bot.answer_callback_query(call.id, f"🍬 رادمهر {p}% پاستیله!\nرسماً داره به جای خون، ژله تو رگاش می‌چرخه! 😂", show_alert=True)

    # --- منوی پیشرفته رئیس حسین پاستیل ---
    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(f"💰 موجودی: {stats['pastils']} پاستیل", callback_data='show_stats_alert'),
            types.InlineKeyboardButton("🎮 شروع عملیات دزدی", callback_data='game_step1'),
            types.InlineKeyboardButton("🏆 لیست کونی‌های برتر", callback_data='leaderboard'),
            types.InlineKeyboardButton("🛒 فروشگاه تجهیزات", callback_data='game_shop'),
            types.InlineKeyboardButton("➕ دریافت پاستیل (خرید/دعوت)", callback_data='get_pastil_list'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr')
        )
        cap = f"🕶 <b>پنل مدیریت عملیات رئیس حسین</b>\n\n💰 موجودی تو: {stats['pastils']} پاستیل\nرادمهر (پسرش) جلوی در انبار نگهبانی میده!"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/27XKnLBd/image.png", caption=cap, parse_mode="HTML", reply_markup=boss_markup)

    elif call.data == "show_stats_alert":
        bot.answer_callback_query(call.id, f"موجودی شما: {stats['pastils']} پاستیل 🍭", show_alert=True)

    # --- لیست روش‌های کسب پاستیل ---
    elif call.data == "get_pastil_list":
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("🤝 دعوت از دوستان (۵۰ پاستیل)", callback_data='invite_friends'),
            types.InlineKeyboardButton("💳 خرید با پول واقعی", callback_data='buy_money'),
            types.InlineKeyboardButton("🚕 کارگری در اسنپ (۳ پاستیل)", callback_data='work_snap'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss')
        )
        text = ("📜 <b>لیست روش‌های کسب پاستیل:</b>\n\n"
                "1️⃣ <b>دعوت:</b> لینک اختصاصی بگیر و بفرست واسه دوستات.\n"
                "2️⃣ <b>خرید:</b> پکیج‌های پاستیل رو با کارت به کارت بخر.\n"
                "3️⃣ <b>کارگری:</b> برو ماشین رادین رو بشور ۳ تا بگیر!")
        bot.edit_message_caption(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "invite_friends":
        link = f"https://t.me/{(bot.get_me()).username}?start=ref_{user_id}"
        bot.send_message(call.message.chat.id, f"📥 <b>لینک دعوت تو:</b>\n\n{link}\n\nهر کی با این لینک بیاد ربات، ۵۰ تا پاستیل می‌گیری! 🔥")

    elif call.data == "buy_money":
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ ارسال رسید واریز", url=f"tg://user?id={ADMIN_ID}"), types.InlineKeyboardButton("🔙 بازگشت", callback_data='get_pastil_list'))
        text = ("💎 <b>بسته‌های پاستیل:</b>\n\n"
                "🔸 ۱۰۰ پاستیل: ۱۰ هزار تومان\n"
                "🔸 ۵۰۰ پاستیل: ۴۰ هزار تومان\n"
                "🔸 ۱۰۰۰ پاستیل: ۷۰ هزار تومان\n\n"
                "💳 <b>شماره کارت:</b>\n<code>6219-8619-1556-6334</code>\n"
                "بنام: لیلا حسن پور فرخی\n\n"
                "ارسال رسید برای شارژ الزامیست.")
        bot.edit_message_caption(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "work_snap":
        stats['pastils'] += 3
        bot.answer_callback_query(call.id, "✅ ماشین رادین رو شستی و ۳ تا پاستیل گرفتی! تف تو این زندگی. 😂", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "عملیات تموم شد.", reply_markup=main_menu_inline())

    # --- لیست برترین‌ها ---
    elif call.data == "leaderboard":
        top = sorted(user_data.items(), key=lambda x: x[1]['pastils'], reverse=True)[:10]
        lb = "🏆 <b>۱۰ کونیِ برتر محله (بیشترین پاستیل):</b>\n\n"
        for i, (uid, data) in enumerate(top, 1):
            lb += f"{i}. {data.get('name', 'ناشناس')} ➔ {data['pastils']} پاستیل 🍭\n"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss'))
        bot.edit_message_caption(lb, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    # --- شروع بازی پاستیل دزدی ---
    elif call.data == "game_step1":
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🍭 رشوه به رادمهر (۱ پاستیل)", callback_data='bribe'),
            types.InlineKeyboardButton("👣 رد شدن مخفیانه", callback_data='sneak')
        )
        bot.edit_message_caption("💂 <b>رادمهر جلو در انبار ایستاده!</b>\nچیکار می‌کنی؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "bribe":
        if stats['pastils'] >= 1:
            stats['pastils'] -= 1
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار حسین", callback_data='final_steal'))
            bot.edit_message_caption("✅ رادمهر پاستیل رو گرفت و راه رو باز کرد. برو تو!", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ پاستیل نداری که رشوه بدی گدا!", show_alert=True)

    elif call.data == "sneak":
        chance = 0.8 if stats['shoes'] else 0.4
        if random.random() < chance:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏃 ورود به انبار حسین", callback_data='final_steal'))
            bot.edit_message_caption("✅ ایول! رادمهر چرت می‌زد، رد شدی.", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ رادمهر دیدت! ۵ تا پاستیل جریمه شدی.", show_alert=True)
            stats['pastils'] = max(0, stats['pastils'] - 5)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "شکست خوردی!", reply_markup=main_menu_inline())

    elif call.data == "final_steal":
        stolen = random.randint(5, 25)
        if random.random() > 0.4:
            stats['pastils'] += stolen
            bot.answer_callback_query(call.id, f"💎 ایول! {stolen} پاستیل از حسین دزدیدی!", show_alert=True)
        else:
            if stats['spray']:
                stats['spray'] = False
                bot.answer_callback_query(call.id, "⚠️ حسین بیدار شد ولی اسپری زدی تو چشمش و با پاستیل‌ها فرار کردی!", show_alert=True)
                stats['pastils'] += stolen
            else:
                bot.answer_callback_query(call.id, "❌ حسین بیدار شد و کل پاستیلاتو گرفت! 😂", show_alert=True)
                stats['pastils'] = 0
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "عملیات پایان یافت.", reply_markup=main_menu_inline())

    # --- فروشگاه ---
    elif call.data == "game_shop":
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(f"👟 کفش بی‌صدا (۲۰ پاستیل) {'✅' if stats['shoes'] else ''}", callback_data='buy_shoes'),
            types.InlineKeyboardButton(f"🌶 اسپری فلفل (۱۵ پاستیل) {'✅' if stats['spray'] else ''}", callback_data='buy_spray'),
            types.InlineKeyboardButton("🔙 بازگشت", callback_data='radmehr_boss')
        )
        bot.edit_message_caption(f"🛒 <b>فروشگاه ابزار دزدی</b>\n💰 موجودی: {stats['pastils']}", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "buy_shoes":
        if stats['pastils'] >= 20 and not stats['shoes']:
            stats['pastils'] -= 20
            stats['shoes'] = True
            bot.answer_callback_query(call.id, "✅ خریدی! حالا راحت‌تر از رادمهر رد میشی.", show_alert=True)
            callback_answer(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data='game_shop'))
        else: bot.answer_callback_query(call.id, "❌ موجودی کم یا قبلا خریدی!", show_alert=True)

    elif call.data == "buy_spray":
        if stats['pastils'] >= 15 and not stats['spray']:
            stats['pastils'] -= 15
            stats['spray'] = True
            bot.answer_callback_query(call.id, "✅ خریدی! حسین رو می‌تونی با این کور کنی.", show_alert=True)
            callback_answer(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data='game_shop'))
        else: bot.answer_callback_query(call.id, "❌ موجودی کم یا قبلا خریدی!", show_alert=True)

    # --- سایر بخش‌های قدیمی ---
    elif call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="🍑 ویس سهیل همدونی بدبخت", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    elif call.data == "radin_hole":
        rd_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💨 سنجش میزان گوزو بودن", callback_data='rate_radin_fart'),
            types.InlineKeyboardButton("🔙 بازگشت به اسنپ", callback_data='back_to_snap_list')
        )
        cap = "👤 <b>پرونده: رادین هول</b>\n\n📝 راننده اسنپ بدبو! 💨"
        bot.send_photo(call.message.chat.id, "https://i.ibb.co/5WQy7Vqh/image.png", caption=cap, parse_mode="HTML", reply_markup=rd_markup)

    elif call.data == "rate_radin_fart":
        bot.answer_callback_query(call.id, f"⚠️ رادین هول {random.randint(75, 100)}% گوزوئه!", show_alert=True)

    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی اصلی:", reply_markup=main_menu_inline())

    elif call.data == "back_to_snap_list":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "🚕 اسنپ اوشاخلاری:", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole')))

    elif call.data == "report":
        msg = bot.send_message(call.message.chat.id, "📝 اسم کونی مورد نظر و جرمش رو بنویس:")
        bot.register_next_step_handler(msg, save_report)

    bot.answer_callback_query(call.id)

def save_report(message):
    bot.send_message(ADMIN_ID, f"🚩 گزارش جدید:\n👤 از: {message.from_user.first_name}\n📝 متن: {message.text}")
    bot.reply_to(message, "✅ حله، شومبول علی ردیفش می‌کنه!")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
