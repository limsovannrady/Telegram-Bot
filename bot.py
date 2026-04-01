import os
from telegram import Update, constants, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from deep_translator import GoogleTranslator

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

all_users = {}

LANGUAGES = {
    "km": "🇰🇭 ខ្មែរ",
    "en": "🇺🇸 អង់គ្លេស",
    "zh-CN": "🇨🇳 ចិន",
    "ja": "🇯🇵 ជប៉ុន",
    "ko": "🇰🇷 កូរ៉េ",
    "fr": "🇫🇷 បារាំង",
    "th": "🇹🇭 ថៃ",
    "vi": "🇻🇳 វៀតណាម",
    "de": "🇩🇪 អាល្លឺម៉ង់",
    "es": "🇪🇸 អេស្ប៉ាញ",
    "ru": "🇷🇺 រុស្សី",
    "ar": "🇸🇦 អារ៉ាប់",
    "pt": "🇵🇹 ព័រទុយហ្គាល់",
    "it": "🇮🇹 អ៊ីតាលី",
    "hi": "🇮🇳 ហិណ្ឌូ",
    "id": "🇮🇩 អ៊ីនដូនេស៊ី",
    "ms": "🇲🇾 ម៉ាឡេស៊ី",
    "tl": "🇵🇭 ហ្វីលីពីន",
    "tr": "🇹🇷 តួគី",
    "nl": "🇳🇱 ហូឡង់",
    "pl": "🇵🇱 ប៉ូឡូញ",
    "uk": "🇺🇦 អ៊ុយក្រែន",
    "sv": "🇸🇪 ស៊ុយអែត",
    "da": "🇩🇰 ដាណឺម៉ាក",
    "fi": "🇫🇮 ហ្វាំងឡង់",
    "no": "🇳🇴 នន័រវែស",
    "cs": "🇨🇿 ឆែក",
    "ro": "🇷🇴 រូម៉ានី",
    "hu": "🇭🇺 ហុងគ្រី",
    "el": "🇬🇷 ក្រិច",
    "he": "🇮🇱 អ៊ីស្រាអែល",
    "fa": "🇮🇷 ហ្វ័រស៊ី",
    "bn": "🇧🇩 បង់ក្លាដែស",
    "ur": "🇵🇰 អ៊ូតូ",
    "sw": "🇰🇪 ស្វាហ៊ីលី",
    "my": "🇲🇲 មីយ៉ាន់ម៉ា",
    "lo": "🇱🇦 ឡាវ",
    "mn": "🇲🇳 ម៉ុងហ្គោល",
    "si": "🇱🇰 ស្រីលង្កា",
    "ne": "🇳🇵 នេប៉ាល់",
}

user_language = {}


def get_language_keyboard(page=0):
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


def track_user(user):
    all_users[user.id] = {
        "id": user.id,
        "name": user.full_name,
        "username": f"@{user.username}" if user.username else "គ្មាន",
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update.effective_user)
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(
        f"សួស្តី {update.effective_user.first_name} 👋\n\n"
        f"👉 /language ដើម្បីជ្រើសរើសភាសាបកប្រែ។",
        reply_markup=ForceReply(selective=False),
        do_quote=True
    )


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(
        "🌐 សូមជ្រើសរើសភាសាដែលអ្នកចង់បកប្រែទៅ៖",
        reply_markup=get_language_keyboard(),
        do_quote=True
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, lang_code)
    user_language[query.from_user.id] = lang_code

    await query.message.delete()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"✅ បកប្រែទៅភាសា {lang_name}",
        reply_markup=ForceReply(selective=False)
    )


async def see_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ អ្នកមិនមានសិទ្ធិប្រើ command នេះទេ។", do_quote=True)
        return
    if not all_users:
        await update.message.reply_text("📭 មិនទាន់មាន user ប្រើប្រាស់ bot នៅឡើយ។", do_quote=True)
        return
    lines = [f"👥 Users ទាំងអស់ ({len(all_users)} នាក់):\n"]
    for i, u in enumerate(all_users.values(), 1):
        lines.append(f"{i}. {u['name']} | {u['username']} | ID: {u['id']}")
    await update.message.reply_text("\n".join(lines), do_quote=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update.effective_user)
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    user_id = update.effective_user.id
    text = update.message.text
    target_lang = user_language.get(user_id, "km")

    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        await update.message.reply_text(
            translated,
            do_quote=True
        )
    except Exception:
        await update.message.reply_text(
            "❌ សូមទោស មានបញ្ហាក្នុងការបកប្រែ។ សូមព្យាយាមម្តងទៀត។",
            do_quote=True
        )


async def change_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "🌐 សូមជ្រើសរើសភាសាដែលអ្នកចង់បកប្រែទៅ៖",
        reply_markup=get_language_keyboard(0)
    )


async def post_init(application):
    from telegram import BotCommand
    await application.bot.set_my_commands([
        BotCommand("start", "ចាប់ផ្តើមប្រើ Bot"),
        BotCommand("language", "ជ្រើសរើសភាសាបកប្រែ"),
    ])


def create_app():
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("see", see_command))
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(change_lang_callback, pattern="^change_lang$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application


if __name__ == "__main__":
    create_app().run_polling()
