TOKEN = "6315511699:AAGquUxZkmx0eJqQjjoYBmrwMg-VufmKejg"

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import mongodb 

def get_markup(user_data):
    return [
        [
            InlineKeyboardButton(f"MHA {'✅' if user_data.get('MHA') else '❔'}", callback_data="MHA"),
            InlineKeyboardButton(f"JJK {'✅' if user_data.get('JJK') else '❔'}", callback_data="JJK"),
            InlineKeyboardButton(f"OP {'✅' if user_data.get('OP') else '❔'}", callback_data="OP"),
        ],
        [InlineKeyboardButton("Done", callback_data="0")]
    ]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not mongodb.get_by_chat_id(update.effective_chat.id):
        mongodb.save_user_info(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text = "Hi this is a bot for getting manga updates from website tcbscans.com")

async def sub_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(get_markup({}))

    await update.message.reply_text("Choose titles to subscribe:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    if query.data != '0':
        context.user_data[query.data] = not context.user_data.get(query.data)
        reply_markup = InlineKeyboardMarkup(get_markup(context.user_data))
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    else:
        titles = [t[0] for t in  context.user_data.items() if t[1]]
        context.user_data.clear()
        mongodb.update_user_titles(context._chat_id, titles)
        await query.edit_message_text(text="Choices saved")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start_command)
    sub_handler = CommandHandler('sub', sub_command)
    application.add_handlers([start_handler, sub_handler])
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
