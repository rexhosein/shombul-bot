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

    # رئیس حسین پاستیل (عکس جدید + بازی)
    elif call.data == "radmehr_boss":
        boss_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💉 تست تستسترون ابوی", callback_data='dad_test'),
            types.InlineKeyboardButton("🎮 بازی: دزدیدن پاستیل از ماتحت حسین", callback_data='game_pastil'),
            types.InlineKeyboardButton("🔙 بازگشت به رادمهر", callback_data='radmehr')
        )
        cap = "🕶 <b>اطلاعات فوق محرمانه: رئیس حسین پاستیل</b>\n\n⚖️ <b>جرم:</b> قاچاق پاستیل‌های تاریخ مصرف گذشته و خوردنِ پاستیلِ ملت!\n⚠️ <b>توضیحات:</b> ایشون جوری پاستیل می‌خوره که انگار فردا قراره شکر تو دنیا تموم بشه! رئیس کل کونی‌های شیرین‌خور منطقه!"
        bot.send_photo(call.message.chat.id, "https://ibb.co/27XKnLBd", caption=cap, parse_mode="HTML", reply_markup=boss_markup)

    elif call.data == "game_pastil":
        res = random.choice(['win', 'lose', 'lose_bad'])
        if res == 'win':
            bot.answer_callback_query(call.id, "✅ ایول! یه پاستیل خرسی از جیب حسین دزدیدی و اون کونی اصلاً نفهمید! نوش جان 🍭", show_alert=True)
        elif res == 'lose':
            bot.answer_callback_query(call.id, "❌ حسین پاستیل مچتو گرفت! جوری زد پس کله‌ات که مزه پاستیل از یادت رفت بچه کونی! 😂", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ شکست خوردی! حسین پاستیل بیدار شد و رید به هیکلت کونیِ دزد! 💩", show_alert=True)

    elif call.data == "dad_test":
        p = random.randint(1, 15)
        bot.answer_callback_query(call.id, f"🧪 نتیجه آزمایش تستسترون ابوی:\nمقدار: {p}% (در حد جلبک دریایی!) 📉\nنیاز به پیوند تخم فوری!", show_alert=True)

    # سهیل همدونی
    elif call.data == "soheil":
        v_id = "AwACAgQAAxkBAAN8aZBGtgpzhVI42sy6OQSEpuo1fHoAAqkgAAKQeYFQa2nLJ52gz9Y6BA"
        bot.send_voice(call.message.chat.id, v_id, caption="🍑 ویس سهیل همدونی بدبخت", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 بازگشت", callback_data='back_to_main')))

    # رادین هول
    elif call.data == "radin_hole":
        rd_markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💨 سنجش میزان گوزو بودن", callback_data='rate_radin_fart'),
            types.InlineKeyboardButton("🔙 بازگشت به اسنپ", callback_data='back_to_snap_list')
        )
        cap = (f"👤 <b>پرونده: رادین هول</b>\n\n"
               f"📝 <b>توضیحات:</b> راننده اسنپی که اگه تو ماشینش بشینی بوی جوراب و گوز خفه ات می‌کنه! 💨\n\n"
               f"💖 <b>لیست سوراخ‌ها (Ex):</b>\n❌ سلنا، النا، سیما، شیما، فاطی و ...\n\n"
               f"⚠️ <b>هشدار:</b> به دلیل نشت شدید گاز، فندک نزنید!")
        bot.send_photo(call.message.chat.id, "https://ibb.co/5WQy7Vqh", caption=cap, parse_mode="HTML", reply_markup=rd_markup)

    elif call.data == "rate_radin_fart":
        p = random.randint(75, 100)
        bot.answer_callback_query(call.id, f"⚠️ هشدار زیست‌محیطی:\nرادین هول {p}% گوزوئه! \nخطر مرگ در اثر استنشاق گازهای سمی! 😷", show_alert=True)

    # بازگشت‌ها
    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی انتخاب سوژه‌ها:", reply_markup=main_menu_inline())

    elif call.data == "back_to_snap_list":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        snap_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🕳 رادین هول", callback_data='radin_hole'))
        bot.send_message(call.message.chat.id, "🚕 لیست رانندگان اسنپ اوشاخلاری:", reply_markup=snap_markup)

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

