import os
import telebot
from telebot import types

# ==========================================
# TOKEN
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN ёфт нашуд!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


# ==========================================
# КАНАЛҲО БАРОИ ПОДПИСКА
# ==========================================
#
# Мисол:
# "@mychannel"
#
# Бот бояд дар канал Administrator бошад.
#

CHANNELS = [
    "https://t.me/khamai_bozikho"
]


# ==========================================
# БОЗИҲО
# ==========================================

games = [
    (
        "Minecraft",
        "https://play.google.com/store/search?q=Minecraft&c=apps"
    ),
    (
        "Roblox",
        "https://play.google.com/store/search?q=Roblox&c=apps"
    ),
    (
        "Free Fire",
        "https://play.google.com/store/search?q=Free%20Fire&c=apps"
    ),
    (
        "PUBG Mobile",
        "https://play.google.com/store/search?q=PUBG%20Mobile&c=apps"
    ),
    (
        "Brawl Stars",
        "https://play.google.com/store/search?q=Brawl%20Stars&c=apps"
    ),
    (
        "Clash of Clans",
        "https://play.google.com/store/search?q=Clash%20of%20Clans&c=apps"
    ),
    (
        "Clash Royale",
        "https://play.google.com/store/search?q=Clash%20Royale&c=apps"
    ),
    (
        "Subway Surfers",
        "https://play.google.com/store/search?q=Subway%20Surfers&c=apps"
    ),
    (
        "Hill Climb Racing",
        "https://play.google.com/store/search?q=Hill%20Climb%20Racing&c=apps"
    ),
    (
        "Asphalt 9",
        "https://play.google.com/store/search?q=Asphalt%209&c=apps"
    ),
]


# ==========================================
# САНҶИШИ ПОДПИСКА
# ==========================================

def is_subscribed(user_id):
    """
    Санҷиш мекунад, ки корбар ба ҳамаи каналҳо
    подписка кардааст ё не.
    """

    for channel in CHANNELS:

        try:
            member = bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except Exception as error:

            print(
                f"Subscription check error for {channel}: {error}"
            )

            return False

    return True


# ==========================================
# КЛАВИАТУРАИ ПОДПИСКА
# ==========================================

def subscription_keyboard():

    keyboard = types.InlineKeyboardMarkup()

    for number, channel in enumerate(CHANNELS, 1):

        username = channel.replace("@", "")

        keyboard.add(
            types.InlineKeyboardButton(
                text=f"📢 Канал {number}",
                url=f"https://t.me/{username}"
            )
        )

    keyboard.add(
        types.InlineKeyboardButton(
            text="✅ Ман подписка кардам",
            callback_data="check_subscription"
        )
    )

    return keyboard


# ==========================================
# ПАЁМИ ПОДПИСКА
# ==========================================

def subscription_message(chat_id):

    bot.send_message(
        chat_id,

        "🔒 <b>Дастрасӣ маҳдуд аст!</b>\n\n"
        "Барои истифодаи бот аввал ба канали мо "
        "подписка кунед.\n\n"
        "1️⃣ Ба канал дароед\n"
        "2️⃣ Subscribe / Подписаться-ро пахш кунед\n"
        "3️⃣ Баъд «✅ Ман подписка кардам»-ро пахш кунед",

        reply_markup=subscription_keyboard()
    )


# ==========================================
# САНҶИШ ПЕШ АЗ ИСТИФОДА
# ==========================================

def require_subscription(message):

    if is_subscribed(message.from_user.id):
        return True

    subscription_message(message.chat.id)

    return False


# ==========================================
# МЕНЮ
# ==========================================

def main_menu():

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    keyboard.row(
        "🎮 Ҳамаи бозиҳо",
        "🔎 Ҷустуҷӯи бозӣ"
    )

    return keyboard


# ==========================================
# START
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):

    if not is_subscribed(message.from_user.id):

        subscription_message(message.chat.id)

        return

    bot.send_message(
        message.chat.id,

        "🎮 <b>Салом!</b>\n\n"
        "Ба Game Bot хуш омадед!\n\n"
        "Бозиро метавонед бо рақам ё ном ҷустуҷӯ кунед.",

        reply_markup=main_menu()
    )


# ==========================================
# CALLBACK: САНҶИШИ ПОДПИСКА
# ==========================================

@bot.callback_query_handler(
    func=lambda call: call.data == "check_subscription"
)
def check_subscription(call):

    user_id = call.from_user.id

    if is_subscribed(user_id):

        bot.answer_callback_query(
            call.id,
            "✅ Подписка тасдиқ шуд!"
        )

        bot.send_message(
            call.message.chat.id,

            "🎉 <b>Подписка тасдиқ шуд!</b>\n\n"
            "Акнун бот барои шумо кушода аст.",

            reply_markup=main_menu()
        )

    else:

        bot.answer_callback_query(
            call.id,
            "❌ Аввал ба канал подписка кунед.",
            show_alert=True
        )


# ==========================================
# ҲАМАИ БОЗИҲО
# ==========================================

@bot.message_handler(
    func=lambda message:
        message.text == "🎮 Ҳамаи бозиҳо"
)
def all_games(message):

    if not require_subscription(message):
        return

    text = "🎮 <b>Рӯйхати бозиҳо:</b>\n\n"

    for number, (name, link) in enumerate(games, 1):

        text += (
            f"<b>{number}.</b> "
            f"<a href=\"{link}\">{name}</a>\n"
        )

    text += (
        "\n🔢 Рақами бозиро нависед.\n"
        "🔎 Ё номи бозиро ҷустуҷӯ кунед."
    )

    bot.send_message(
        message.chat.id,
        text,
        disable_web_page_preview=True
    )


# ==========================================
# ТУГМАИ ҶУСТУҶӮ
# ==========================================

@bot.message_handler(
    func=lambda message:
        message.text == "🔎 Ҷустуҷӯи бозӣ"
)
def search_help(message):

    if not require_subscription(message):
        return

    bot.send_message(
        message.chat.id,

        "🔎 <b>Ҷустуҷӯи бозӣ</b>\n\n"
        "Номи бозӣ ё рақами онро нависед.\n\n"
        "Мисол:\n"
        "Minecraft\n"
        "Roblox\n"
        "5"
    )


# ==========================================
# ҶУСТУҶӮ БО НОМ Ё РАҚАМ
# ==========================================

@bot.message_handler(func=lambda message: True)
def find_game(message):

    if not require_subscription(message):
        return

    query = message.text.strip().lower()

    # ======================================
    # ҶУСТУҶӮ БО РАҚАМ
    # ======================================

    if query.isdigit():

        number = int(query)

        if 1 <= number <= len(games):

            name, link = games[number - 1]

            bot.send_message(
                message.chat.id,

                f"🎮 <b>{number}. {name}</b>\n\n"
                f"🔗 <a href=\"{link}\">"
                f"Кушодани бозӣ"
                f"</a>",

                disable_web_page_preview=False
            )

        else:

            bot.send_message(
                message.chat.id,

                f"❌ Бозии рақами <b>{number}</b> вуҷуд надорад.\n\n"
                f"Дар ҳозир бот {len(games)} бозӣ дорад."
            )

        return

    # ======================================
    # ҶУСТУҶӮ БО НОМ
    # ======================================

    found = []

    for number, (name, link) in enumerate(games, 1):

        if query in name.lower():

            found.append(
                (number, name, link)
            )

    # ======================================
    # НАТИҶА
    # ======================================

    if found:

        text = "🔎 <b>Бозиҳои ёфтшуда:</b>\n\n"

        for number, name, link in found:

            text += (
                f"<b>{number}.</b> "
                f"<a href=\"{link}\">{name}</a>\n"
            )

        bot.send_message(
            message.chat.id,
            text,
            disable_web_page_preview=True
        )

    else:

        bot.send_message(
            message.chat.id,

            "❌ <b>Бозӣ ёфт нашуд.</b>\n\n"
            "Номи бозиро дуруст нависед ё "
            "«🎮 Ҳамаи бозиҳо»-ро пахш кунед."
        )


# ==========================================
# BOT START
# ==========================================

print("===================================")
print("🤖 Telegram Game Bot started!")
print(f"🎮 Games: {len(games)}")
print(f"📢 Channels: {len(CHANNELS)}")
print("===================================")

bot.infinity_polling(
    timeout=60,
    long_polling_timeout=60
)
