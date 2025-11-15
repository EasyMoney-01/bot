import os
import requests
import asyncio
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


# -------------------- SCRAPER --------------------
def scrape_vehicle(num: str):
    try:
        headers = {"User-Agent": generate_user_agent()}
        url = f"https://vahanx.in/rc-search/{num}"

        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        data = {}

        fields = [
            "Owner Name", "Father's Name", "Model Name", "Vehicle Class",
            "Fuel Type", "Registration Date", "Insurance Company", "Registered RTO"
        ]

        for field in fields:
            span = soup.find("span", string=field)
            if not span:
                continue

            parent = span.find_parent("div")
            if not parent:
                continue

            p = parent.find("p")
            if p:
                value = p.get_text(strip=True)

                # Custom owner prefix (requested)
                if field == "Owner Name":
                    value = "DARK SHADOW " + value

                data[field] = value

        return data or None
    except Exception as e:
        print("Scraper Error:", e)
        return None


# -------------------- START COMMAND --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = [[InlineKeyboardButton("🔍 Extract Vehicle Number", callback_data="extract")]]
    markup = InlineKeyboardMarkup(button)

    await update.message.reply_text(
        "🚗 *Vehicle Information Bot*\n\n"
        "Send any vehicle number to get details.",
        reply_markup=markup,
        parse_mode="Markdown"
    )


# -------------------- BUTTON HANDLER --------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "extract":
        await query.edit_message_text(
            "🔢 Send any vehicle number like:\n`MH12AB1234`",
            parse_mode="Markdown"
        )


# -------------------- MESSAGE HANDLER --------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.upper().strip()

    if len(num) < 5:
        await update.message.reply_text("❌ Invalid vehicle number.")
        return

    msg = await update.message.reply_text("⏳ Fetching details...")

    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(None, scrape_vehicle, num)

    if not data:
        await msg.edit_text("❌ No data found or scraping error.")
        return

    result = f"🚗 *Vehicle:* `{num}`\n\n"
    for k, v in data.items():
        result += f"• *{k}:* {v}\n"

    await msg.edit_text(result, parse_mode="Markdown")


# -------------------- MAIN APP --------------------
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot running...")
    await app.run_polling()


# -------------------- ENTRY POINT (WINDOWS SAFE) --------------------
if __name__ == "__main__":
    # DO NOT USE asyncio.run() → causes Windows error
    asyncio.get_event_loop().run_until_complete(main())
