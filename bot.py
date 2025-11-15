import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

def get_vehicle_info(num):
    try:
        ua = generate_user_agent()
        headers = {"User-Agent": ua}
        url = f"https://vahanx.in/rc-search/{num}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {}
        fields = [
            "Owner Name", "Father's Name", "Model Name", "Vehicle Class", 
            "Fuel Type", "Registration Date", "Insurance Company", "Registered RTO"
        ]
        
        for field in fields:
            span = soup.find("span", string=field)
            if span:
                parent = span.find_parent("div")
                if parent:
                    p_tag = parent.find("p")
                    if p_tag:
                        data[field] = p_tag.get_text(strip=True)
        
        return data
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "🤖 *VEHICLE INFO BOT*\n\n"
            "🛠️ *MADE BY DARK SHADOW* 🛠️\n\n"
            "🚗 *How to Use:*\n"
            "Send vehicle number like:\n"
            "• DL01AB1234\n"
            "• KA05CD5678\n"
            "• MH12EF9012\n\n"
            "🔍 I'll fetch vehicle details for you!\n\n"
            "_MADE BY DARK SHADOW_",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        vehicle_number = update.message.text.upper().strip()
        
        if len(vehicle_number) < 5:
            await update.message.reply_text("❌ Please enter a valid vehicle number\n\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
            return
        
        processing_msg = await update.message.reply_text("🔍 *Searching vehicle information...*\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
        
        vehicle_data = get_vehicle_info(vehicle_number)
        
        if not vehicle_data:
            await processing_msg.edit_text("❌ *No data found for this vehicle*\n\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
            return
        
        response = f"🚗 *Vehicle Information*\n\n🔢 *Vehicle Number:* `{vehicle_number}`\n\n"
        
        found_data = False
        for key, value in vehicle_data.items():
            if value:
                response += f"• *{key}:* `{value}`\n"
                found_data = True
        
        if not found_data:
            response = "❌ *No information found for this vehicle*"
        
        response += "\n\n🛠️ _MADE BY DARK SHADOW_"
        
        await processing_msg.edit_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("❌ *Error processing request*\n\n_MADE BY DARK SHADOW_", parse_mode='Markdown')

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🤖 Starting Vehicle Info Bot")
    logger.info("🛠️ MADE BY DARK SHADOW")
    logger.info("🚀 Bot is running...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
