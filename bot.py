import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import logging
import os
from dotenv import load_dotenv
import html
from datetime import datetime

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Code By : @sarthx_bot
def get_vehicle_info(num):
    """
    Function to scrape vehicle information from vahanx.in
    """
    try:
        ua = generate_user_agent()
        h = {
            "User-Agent": ua,
        }
        c = f"https://vahanx.in/rc-search/{num}"
        r = requests.get(c, headers=h)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Code By : @sarthx_bots
        data = {
            "Owner Name": None,
            "Father's Name": None,
            "Owner Serial No": None,
            "Model Name": None,
            "Maker Model": None,
            "Vehicle Class": None,
            "Fuel Type": None,
            "Fuel Norms": None,
            "Registration Date": None,
            "Insurance Company": None,
            "Insurance No": None,
            "Insurance Expiry": None,
            "Insurance Upto": None,
            "Fitness Upto": None,
            "Tax Upto": None,
            "PUC No": None,
            "PUC Upto": None,
            "Financier Name": None,
            "Registered RTO": None,
            "Address": None,
            "City Name": None,
            "Phone": None
        }
        
        # Code By : @sarthx_bots
        for label in data:
            div = soup.find("span", string=label)
            if div:
                parent_div = div.find_parent("div")
                if parent_div:
                    p_tag = parent_div.find("p")
                    if p_tag:
                        data[label] = p_tag.get_text(strip=True)
        
        return data
    except Exception as e:
        logger.error(f"Error fetching vehicle info: {e}")
        return None

def create_main_menu():
    """Create modern inline keyboard menu"""
    keyboard = [
        [InlineKeyboardButton("🚗 Search Vehicle", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("📖 How to Use", callback_data="help"),
         InlineKeyboardButton("👤 About", callback_data="about")],
        [InlineKeyboardButton("🔍 Example Search", callback_data="example")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a modern welcome message when the command /start is issued."""
    user = update.effective_user
    
    # Modern welcome message with dark shadow theme
    welcome_message = f"""
╔═══════════════════════╗
    🚗 *DARK SHADOW VEHICLE BOT* 🚗
╚═══════════════════════╝

┌─────────────────────────┐
   👋 *Welcome {user.first_name}!*
└─────────────────────────┘

*OWNER: DARK SHADOW*
*Developer:* @sarthx_bot

🌙 *Dark Shadow Edition* - Premium Vehicle Intelligence

🔮 *I can reveal hidden vehicle secrets:*
• 🕵️ Owner Identity & Details
• 📊 Vehicle Specifications  
• 🛡️ Insurance Information
• 📜 Registration History
• ⚡ Fitness & Tax Status

✨ *Simply send me a vehicle number to begin the search!*
    """
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='Markdown',
        reply_markup=create_main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send modern help message."""
    help_text = """
╔═══════════════════════╗
       📖 *DARK SHADOW GUIDE*
╚═══════════════════════╝

┌─────────────────────────┐
        🚀 *QUICK START*
└─────────────────────────┘

📝 *Send Vehicle Number Like:*
• `DL01AB1234`
• `KA05CD5678` 
• `MH12EF9012`

┌─────────────────────────┐
        🛠️ *COMMANDS*
└─────────────────────────┘

/start - Wake the Shadow Bot
/help  - Reveal secrets guide  
/about - Know the creator

┌─────────────────────────┐
        🔍 *SEARCH TIPS*
└─────────────────────────┘

• Use correct format: **ST** + **NN** + **AA** + **NNNN**
• No spaces between characters
• Case insensitive

*Example:* `DL01AB1234`

🌙 *Powered by Dark Shadow Technology*
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu"),
         InlineKeyboardButton("🚗 Search Now", switch_inline_query_current_chat="")]
    ]
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            help_text, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            help_text, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send modern about message."""
    about_text = """
╔═══════════════════════╗
        👤 *SHADOW PROFILE*
╚═══════════════════════╝

┌─────────────────────────┐
        🎭 *IDENTITY*
└─────────────────────────┘

*NAME:* DARK SHADOW
*CREATOR:* @sarthx_bot
*VERSION:* Shadow Edition v2.0
*POWER:* Vehicle Intelligence

┌─────────────────────────┐
        🌟 *FEATURES*
└─────────────────────────┘

• 🕵️ Stealth Data Extraction
• 🚀 Lightning Fast Search  
• 📱 Modern Dark Interface
• 🔒 Secure & Private
• 💡 Advanced Algorithms

┌─────────────────────────┐
        ⚡ *TECHNOLOGY*
└─────────────────────────┘

• Python Magic 🐍
• BeautifulSoup Alchemy 
• Telegram Bot API
• Dark Shadow Protocols

*« In the shadows, we find the truth »*
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"),
         InlineKeyboardButton("📖 Guide", callback_data="help")]
    ]
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            about_text, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            about_text, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_vehicle_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle vehicle number input with modern UI."""
    vehicle_number = update.message.text.upper().strip()
    
    # Basic validation
    if len(vehicle_number) < 5:
        error_msg = """
❌ *Invalid Vehicle Number*

Please enter a valid format:
• `DL01AB1234`
• `KA05CD5678`
• Minimum 5 characters required
        """
        await update.message.reply_text(error_msg, parse_mode='Markdown')
        return
    
    # Modern processing message
    processing_msg = await update.message.reply_text("""
🔮 *Dark Shadow is searching...*

╔═══════════════════════╗
   SCANNING DATABASES
╚═══════════════════════╝

• Initiating stealth protocols...
• Accessing vehicle matrix...
• Decrypting information...
    """, parse_mode='Markdown')
    
    try:
        vehicle_data = get_vehicle_info(vehicle_number)
        
        if vehicle_data is None:
            await processing_msg.edit_text("""
🌑 *Shadow Connection Failed*

╔═══════════════════════╗
     NETWORK ERROR
╚═══════════════════════╝

The shadows are silent... 
Please try again later.
            """, parse_mode='Markdown')
            return
        
        valid_data = {k: v for k, v in vehicle_data.items() if v is not None}
        
        if not valid_data:
            await processing_msg.edit_text(f"""
🔍 *No Shadows Found*

╔═══════════════════════╗
    SEARCH RESULTS: NULL
╚═══════════════════════╝

*Vehicle:* `{vehicle_number}`
*Status:* No information in the shadows

💡 *Tips:*
• Check number format
• Try different combinations
• Ensure vehicle is registered
            """, parse_mode='Markdown')
            return
        
        # Modern formatted response
        response = f"""
╔═══════════════════════╗
   🚗 VEHICLE INTEL REPORT
╚═══════════════════════╝

🔢 *TARGET:* `{vehicle_number}`
📅 *SCAN DATE:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌙 *AGENT:* DARK SHADOW

┌─────────────────────────┐
        👤 OWNER DETAILS
└─────────────────────────┘
"""
        
        # Owner details first
        owner_fields = ["Owner Name", "Father's Name", "Owner Serial No", "Address", "City Name", "Phone"]
        for field in owner_fields:
            if vehicle_data.get(field):
                icon = "👤" if "Owner" in field else "🏠" if "Address" in field else "📞" if "Phone" in field else "📍"
                response += f"• {icon} *{field}:* `{vehicle_data[field]}`\n"
        
        response += """
┌─────────────────────────┐
        🚘 VEHICLE SPECS
└─────────────────────────┘
"""
        # Vehicle details
        vehicle_fields = ["Model Name", "Maker Model", "Vehicle Class", "Fuel Type", "Fuel Norms", "Registered RTO"]
        for field in vehicle_fields:
            if vehicle_data.get(field):
                icon = "🚙" if "Model" in field else "⚙️" if "Maker" in field else "🎯" if "Class" in field else "⛽" if "Fuel" in field else "🏛️"
                response += f"• {icon} *{field}:* `{vehicle_data[field]}`\n"
        
        response += """
┌─────────────────────────┐
        📜 DOCUMENTS
└─────────────────────────┘
"""
        # Document details
        doc_fields = ["Registration Date", "Insurance Company", "Insurance Upto", "Fitness Upto", "Tax Upto", "PUC Upto"]
        for field in doc_fields:
            if vehicle_data.get(field):
                icon = "📅" if "Date" in field else "🛡️" if "Insurance" in field else "✅" if "Fitness" in field else "💰" if "Tax" in field else "🌿"
                response += f"• {icon} *{field}:* `{vehicle_data[field]}`\n"
        
        response += """
╔═══════════════════════╗
   🌙 SEARCH COMPLETE
╚═══════════════════════╝
*« The shadows have spoken »*
        """
        
        # Create action buttons
        keyboard = [
            [InlineKeyboardButton("🔍 Search Again", switch_inline_query_current_chat="")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"),
             InlineKeyboardButton("📊 Full Report", callback_data=f"full_{vehicle_number}")]
        ]
        
        await processing_msg.edit_text(
            response, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Error in handle_vehicle_number: {e}")
        await processing_msg.edit_text(""⚡ *Shadow System Overload*

╔═══════════════════════╗
    SYSTEM MALFUNCTION
╚═══════════════════════╝

The dark forces are unstable...
Please try again in a moment.

*Error Code:* SHADOW-001
        """, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "main_menu":
        await start(update, context)
    elif data == "help":
        await help_command(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "example":
        example_msg = """
🔍 *Example Search:*

Try these formats:
• `DL01AB1234`
• `KA05CD5678` 
• `MH12EF9012`
• `TN09GH3456`

💡 *Tip:* Use your actual vehicle number for real results!
        """
        keyboard = [
            [InlineKeyboardButton("🚗 Try Search", switch_inline_query_current_chat="")],
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ]
        await query.message.edit_text(
            example_msg, 
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and send a modern error message."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    error_msg = """
🌑 *Shadow System Error*

╔═══════════════════════╗
    CRITICAL FAILURE
╚═══════════════════════╝

The dark network is disrupted...
Please contact @sarthx_bot

*« Even shadows need maintenance »*
    """
    
    if update and update.effective_message:
        await update.effective_message.reply_text(error_msg, parse_mode='Markdown')

def main() -> None:
    """Start the Dark Shadow Bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Handle vehicle numbers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_vehicle_number
    ))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the Bot
    print("""
╔═══════════════════════╗
   🌙 DARK SHADOW BOT ACTIVATED
╚═══════════════════════╝
* Owner: @sarthx_bot
* Status: Running...
* Mode: Stealth Mode Enabled
    """)
    application.run_polling()

if __name__ == '__main__':
    main()