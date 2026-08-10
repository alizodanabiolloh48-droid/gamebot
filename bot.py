import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN ёфт нашуд!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


# =========================
# БОЗИҲО
# =========================

games = [
    ("Minecraft", "https://play.google.com/store/search?q=Minecraft&c=apps"),
    ("Roblox", "https://play.google.com/store/search?q=Roblox&c=apps"),
    ("Free Fire", "https://play.google.com/store/search?q=Free%20Fire&c=apps"),
    ("PUBG Mobile", "https://play.google.com/store/search?q=PUBG%20Mobile&c=apps"),
    ("Brawl Stars", "https://play.google.com/store/search?q=Brawl%20Stars&c=apps"),
    ("Clash of Clans", "https://play.google.com/store/search?q=Clash%20of%20Clans&c=apps"),
    ("Clash Royale", "https://play.google.com/store/search?q=Clash%20Royale&c=apps"),
    ("Subway Surfers", "https://play.google.com/store/search?q=Subway%20Surfers&c=apps"),
    ("Hill Climb Racing", "https://play.google.com/store/search?q=Hill%20Climb%20Racing&c=apps"),
    ("Asphalt 9", "https://play.google.com/store/search?q=Asphalt%209&c=apps"),
]


# =========================
# МЕНЮ
# =========================

def menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        "🎮 Ҳамаи бозиҳо",
        "🔎 Ҷустуҷӯи бозӣ"
    )

    return keyboard


# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "🎮 <b>Салом!</b>\n\n"
        "Ба Game Bot хуш омадед.\n\n"
        "Аз меню бозиро интихоб кунед.",
        reply_markup=menu()
    )


# =========================
# ҲАМАИ БОЗИҲО
# =========================

@bot.message_handler(
    func=lambda message: message.text == "🎮 Ҳамаи бозиҳо"
)
def all_games(message):

    text = "🎮 <b>Рӯйхати бозиҳо:</b>\n\n"

    for number, (name, link) in enumerate(games, 1):

        text += (
            f"<b>{number}.</b> "
            f"<a href=\"{link}\">{name}</a>\n"
        )

    text += "\n🔢 Рақами бозиро нависед."

    bot.send_message(
        message.chat.id,
        text,
        disable_web_page_preview=True
    )


# =========================
# ҶУСТУҶӮ
# =========================

@bot.message_handler(
    func=lambda message: message.text == "🔎 Ҷустуҷӯи бозӣ"
)
def search_help(message):

    bot.send_message(
        message.chat.id,
        "🔎 Номи бозӣ ё рақами онро нависед.\n\n"
        "Мисол:\n"
        "Minecraft\n"
        "5"
    )


# =========================
# ҶУСТУҶӮ БО НОМ Ё РАҚАМ
# =========================

@bot.message_handler(func=lambda message: True)
def find_game(message):

    query = message.text.strip().lower()

    # Ҷустуҷӯ бо рақам
    if query.isdigit():

        number = int(query)

        if 1 <= number <= len(games):

            name, link = games[number - 1]

            bot.send_message(
                message.chat.id,
                f"🎮 <b>{number}. {name}</b>\n\n"
                f"🔗 <a href=\"{link}\">Кушодани бозӣ</a>"
            )

        else:

            bot.send_message(
                message.chat.id,
                "❌ Ин рақами бозӣ вуҷуд надорад."
            )

        return

    # Ҷустуҷӯ бо ном
    found = []

    for number, (name, link) in enumerate(games, 1):

        if query in name.lower():
            found.append((number, name, link))

    if found:

        text = "🔎 <b>Натиҷа:</b>\n\n"

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
            "❌ Бозӣ ёфт нашуд."
        )


# =========================
# BOT
# =========================

print("🤖 Telegram Game Bot started!")

bot.infinity_polling(
    timeout=60,
    long_polling_timeout=60
)
