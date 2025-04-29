from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
from conversation import (
    start_conversation,
    handle_message,
    handle_followup_buttons
)
from feedback import handle_feedback_rating, handle_feedback_comment
from pharmacist import pharmacist_reply_handler
from tnc import start_handler, tnc_response_handler
import os
from keep_alive import keep_alive

# 🌐 Pingable Flask to keep Replit alive
keep_alive()

# Load Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ✅ Terms & Conditions flow
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(tnc_response_handler, pattern="^(agree|disagree)$"))

    # ✅ Main menu selections (meds, ailments, etc.)
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern="^(avail|ailments|products|store)$"))

    # ✅ Follow-up flows and post-consultation actions
    dispatcher.add_handler(CallbackQueryHandler(handle_followup_buttons, pattern="^(pharmacist_request|return_main|end_chat|continue_chat|gen_mc)$"))

    # ✅ User types question or symptom
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # ✅ Feedback handling (if re-enabled)
    dispatcher.add_handler(CallbackQueryHandler(handle_feedback_rating, pattern="^rate_[1-5]$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback_comment))

    # ✅ Manual /reply from pharmacist (legacy)
    dispatcher.add_handler(CommandHandler("reply", pharmacist_reply_handler))

    updater.start_polling()
    print("✅ Dr.Joji is live and running...")
    updater.idle()

if __name__ == "__main__":
    main()
