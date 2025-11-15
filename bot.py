import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import os
from dotenv import load_dotenv
import telebot
import time
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.reply_to(message, 
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
        logger.info(f"Start command from user: {message.chat.id}")
    except Exception as e:
        logger.error(f"Error in start: {e}")

@bot.message_handler(commands=['owner'])
def show_owner(message):
    try:
        bot.reply_to(message,
            "👤 *BOT OWNER INFORMATION*\n\n"
            "✨ *Creator:* DARK SHADOW\n"
            "🛠️ *Made By:* DARK SHADOW\n"
            "🚀 *Developer:* DARK SHADOW\n\n"
            "_This bot is MADE BY DARK SHADOW_",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in owner: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        vehicle_number = message.text.upper().strip()
        
        if len(vehicle_number) < 5:
            bot.reply_to(message, "❌ Please enter a valid vehicle number\n\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
            return
        
        logger.info(f"Searching for vehicle: {vehicle_number}")
        processing_msg = bot.reply_to(message, "🔍 *Searching vehicle information...*\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
        
        vehicle_data = get_vehicle_info(vehicle_number)
        
        if not vehicle_data:
            bot.edit_message_text(
                "❌ *No data found for this vehicle*\n\n"
                "_MADE BY DARK SHADOW_", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode='Markdown'
            )
            return
        
        response = f"🚗 *Vehicle Information*\n\n"
        response += f"🔢 *Vehicle Number:* `{vehicle_number}`\n\n"
        
        found_data = False
        for key, value in vehicle_data.items():
            if value:
                response += f"• *{key}:* `{value}`\n"
                found_data = True
        
        if not found_data:
            response = "❌ *No information found for this vehicle*"
        
        response += "\n\n"
        response += "🛠️ _MADE BY DARK SHADOW_"
        
        bot.edit_message_text(
            response, 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode='Markdown'
        )
        logger.info(f"Data sent for vehicle: {vehicle_number}")
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        try:
            bot.reply_to(message, "❌ *Error processing request*\n\n_MADE BY DARK SHADOW_", parse_mode='Markdown')
        except:
            pass

def start_bot():
    logger.info("🤖 Starting Vehicle Info Bot")
    logger.info("🛠️ MADE BY DARK SHADOW")
    
    while True:
        try:
            logger.info("🚀 Bot polling started...")
            bot.polling(none_stop=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            logger.error(f"❌ Bot crashed: {e}")
            logger.info("🔄 Restarting bot in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    start_bot()
