import os
from telegram import Update, constants, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from deep_translator import GoogleTranslator

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

LANGUAGES = {
    "km": "🇰🇭 ខ្មែរ",
    "en": "🇺🇸 អង់គ្លេស",
    "zh-CN": "🇨🇳 ចិន",
    "ja": "🇯🇵 ជប៉ុន",
    "ko": "🇰🇷 កូរ៉េ",
    "fr": "🇫🇷 បារាំង",
    "th": "🇹🇭 ថៃ",
    "vi": "🇻🇳 វៀតណាម",
}

user_language = {}

def get_language_keyboard():
    buttons = []
    row = []
    for code, name in LANGUAGES.items():
        row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(
        f"សួស្តី {update.effective_user.first_name}! 👋\n"
        f"ខ្ញុំជា Bot បកប្រែភាសា។\n\n"
        f"📝 សូមវាយអក្សរចូលខាងក្រោម ហើយខ្ញុំនឹងបកប្រែឱ្យអ្នក។\n"
        f"🌐 ប្រើ /language ដើម្បីជ្រើសរើសភាសា។",
        reply_markup=ForceReply(selective=True)
    )

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(
        "🌐 សូមជ្រើសរើសភាសាដែលអ្នកចង់បកប្រែទៅ៖",
        reply_markup=get_language_keyboard()
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, lang_code)
    user_language[query.from_user.id] = lang_code

    await query.edit_message_text(
        f"✅ អ្នកបានជ្រើសរើស៖ {lang_name}\n\n"
        f"📝 សូមវាយអក្សរដែលអ្នកចង់បកប្រែ។"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    user_id = update.effective_user.id
    text = update.message.text
    target_lang = user_language.get(user_id, "km")
    lang_name = LANGUAGES.get(target_lang, target_lang)

    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        await update.message.reply_text(
            f"🌐 បកប្រែទៅ {lang_name}៖\n\n{translated}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 ប្តូរភាសា", callback_data="change_lang")]
            ])
        )
    except Exception as e:
        await update.message.reply_text("❌ សូមទោស មានបញ្ហាក្នុងការបកប្រែ។ សូមព្យាយាមម្តងទៀត។")

async def change_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "🌐 សូមជ្រើសរើសភាសាដែលអ្នកចង់បកប្រែទៅ៖",
        reply_markup=get_language_keyboard()
    )

async def post_init(application):
    from telegram import BotCommand
    await application.bot.set_my_commands([
        BotCommand("start", "ចាប់ផ្តើមប្រើ Bot"),
        BotCommand("language", "ជ្រើសរើសភាសាបកប្រែ"),
    ])

app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("language", language_command))
app.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
app.add_handler(CallbackQueryHandler(change_lang_callback, pattern="^change_lang$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
