from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio
import traceback

from SlounikOrgClient import query_dictionary
from Cache import HtmlCache

# Create global cache instance
html_cache = HtmlCache()

# Read the token from a file named "token"
# with open(os.path.join(os.path.dirname(__file__), 'token'), 'r') as f:
#     BOT_TOKEN = f.read().strip()


BOT_TOKEN = os.getenv("MESSAGE_SOURCE_TOKEN")

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добры дзень! Дашліце мне слова, і я спытаю Slounik.org наконт гэтага слова ;)")

# Handler for any non-command text message
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # html_parts = query_dictionary(user_message)
        html_parts = html_cache.cached(user_message, query_dictionary)
        for part in html_parts:
            await update.message.reply_text(part, parse_mode="HTML")
            await asyncio.sleep(1)  # 1 second delay
    except Exception as e:
        # Print the full traceback to console
        print("Error occurred while processing message:")
        traceback.print_exc()
        # print("Sending reply with error message")
        await update.message.reply_text("Выбачайце, нейкая памылка адбылася, калі апрацоўваў ваш запыт :(")
        # print("Done sending reply with error message")


# Create and run the bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()