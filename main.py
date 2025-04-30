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

# ✅ ADD THESE TWO LINES for keep-alive
from keep_alive import app
import threading
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(tnc_response_handler, pattern="^(agree|disagree)$"))
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern="^(avail|ailments|products|store)$"))
    dispatcher.add_handler(CallbackQueryHandler(handle_followup_buttons, pattern="^(pharmacist_request|return_main|end_chat|continue_chat|gen_mc)$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(handle_feedback_rating, pattern="^rate_[1-5]$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback_comment))
    dispatcher.add_handler(CommandHandler("reply", pharmacist_reply_handler))

    updater.start_polling()
    print("✅ Dr.Joji is live and running...")
    updater.idle()

if __name__ == "__main__":
    main()
