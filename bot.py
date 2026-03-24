import os
from telegram import Update, constants, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(
        f"សួស្តី {update.effective_user.first_name}! សូមវាយអក្សរចូលខាងក្រោម៖",
        reply_markup=ForceReply(selective=True)
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
