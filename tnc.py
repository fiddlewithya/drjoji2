# tnc.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils import show_main_menu
from keyboards import tnc_keyboard

TNC_MESSAGE = """*Welcome to DrJoji!*

*Terms & Conditions*

*Medical Disclaimer*  
This chatbot aims to promote a healthy lifestyle as well as provide general health advice and product information only. It is not a substitute for professional medical advice. If you have an urgent and/or serious medical concern, please visit a medical facility.

*PDPA Disclaimer*  
By using this chatbot, you consent to the collection and processing of your data to improve our services. We do not store sensitive medical data or share it without consent, except as required by law."""

def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        TNC_MESSAGE,
        reply_markup=tnc_keyboard(),
        parse_mode="Markdown"
    )

def tnc_response_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    response = query.data

    # ✅ Delete the T&C message
    try:
        query.delete_message()
    except Exception as e:
        print("T&C message deletion failed:", e)

    if response == "agree":
        show_main_menu(user_id, context.bot)
    else:
        context.bot.send_message(
            chat_id=user_id,
            text="❗ You need to agree to the Terms & Conditions before you can use Doctor Joji 🩺\n\nIf you change your mind, just type /start to begin again."
        )


