# handlers.py
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from conversation import (
    start_conversation,
    handle_message,
    handle_followup_buttons
)
from utils import (
    handle_feedback_rating,
    handle_feedback_comment
)

def register_handlers(dispatcher):
    # Start main menu
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern="^(ailments|products|avail|store)$"))

    # Handle after a message is typed
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Handle button presses after consultation
    dispatcher.add_handler(CallbackQueryHandler(handle_followup_buttons, pattern="^(gen_mc|return_main|pharmacist_request|end_chat)$"))

    # Handle feedback ratings
    dispatcher.add_handler(CallbackQueryHandler(handle_feedback_rating, pattern="^rate_[1-5]$"))

    # Handle feedback text comment
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r"^[^/].*"), handle_feedback_comment))
