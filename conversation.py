from telegram import Update
from telegram.ext import CallbackContext
from config import ADMIN_CHAT_ID
from pharma_ai import generate_symptom_response, generate_free_response, generate_rest_days_suggestion
from utils import show_main_menu
from keyboards import (
    followup_options_keyboard,
    return_main_keyboard,
    generate_mc_button
)
from certificate import generate_clean_medical_certificate_v2
from datetime import datetime
import os

conversation_state = {}
user_symptom_message = {}
followup_context = {}
chat_history = {}
awaiting_name = {}
awaiting_nric = {}
temp_user_inputs = {}

def start_conversation(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    context.user_data.clear()

    try:
        query.delete_message()
    except:
        pass

    option = query.data
    conversation_state[user_id] = option
    followup_context[user_id] = False
    chat_history[user_id] = []
    user_symptom_message[user_id] = ""

    if option in ["ailments", "products"]:
        context.bot.send_message(chat_id=user_id, text="💬 What would you like to ask about?")
        return

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    msg = update.message.text.strip()

    # Handle name input for MC
    if awaiting_name.get(user_id):
        temp_user_inputs[user_id] = {"name": msg}
        awaiting_name[user_id] = False
        awaiting_nric[user_id] = True
        context.bot.send_message(chat_id=user_id, text="Please enter your NRIC/FIN:")
        return

    # Handle NRIC input for MC
    if awaiting_nric.get(user_id):
        temp_user_inputs[user_id]["nric"] = msg
        awaiting_nric[user_id] = False

        name = temp_user_inputs[user_id]["name"]
        nric = temp_user_inputs[user_id]["nric"]
        illness = user_symptom_message.get(user_id, "")
        rest_days = suggest_rest_days(illness)

        cert_path = generate_clean_medical_certificate_v2(name, nric, rest_days)
        if os.path.exists(cert_path):
            with open(cert_path, 'rb') as f:
                context.bot.send_document(chat_id=user_id, document=f, filename=os.path.basename(cert_path),
                                          caption="📄 Your Medical Certificate has been generated.")

        context.bot.send_message(chat_id=user_id, text="🔁 Returning to main menu.")
        show_main_menu(user_id, context.bot)
        return

    # Follow-up flow
    if followup_context.get(user_id):
        chat_history.setdefault(user_id, []).append({"role": "user", "content": msg})
        user_symptom_message[user_id] = msg  # ✅ Store latest symptom for MC
        try:
            reply = generate_free_response(user_id, msg, history=chat_history[user_id])
            chat_history[user_id].append({"role": "assistant", "content": reply})
            context.bot.send_message(chat_id=user_id, text=reply)

            # ✅ Show MC option again during follow-up
            context.bot.send_message(
                chat_id=user_id,
                text="Would you like to generate a medical certificate?",
                reply_markup=generate_mc_button()
            )
            return
        except Exception as e:
            print("Free response error:", e)
            context.bot.send_message(chat_id=user_id, text="❌ AI is currently unavailable.")
            return

    # First-time consultation
    user_symptom_message[user_id] = msg
    flow_type = "medication" if conversation_state.get(user_id) == "products" else "symptom"

    try:
        full_prompt = f"User's question: {msg}"
        ai_reply, response_type = generate_symptom_response(full_prompt, force_type=flow_type)
        context.bot.send_message(chat_id=user_id, text=ai_reply, parse_mode='Markdown')

        if conversation_state.get(user_id) == "ailments":
            context.bot.send_message(
                chat_id=user_id,
                text="Would you like to generate a medical certificate?",
                reply_markup=generate_mc_button()
            )
        else:
            context.bot.send_message(
                chat_id=user_id,
                text="Would you like to continue or return to the main menu?",
                reply_markup=followup_options_keyboard()
            )

        followup_context[user_id] = True
        chat_history[user_id] = [{"role": "user", "content": msg}, {"role": "assistant", "content": ai_reply}]

    except Exception as e:
        print("AI error:", str(e))
        context.bot.send_message(chat_id=user_id, text="❌ AI is currently unavailable.")


def handle_followup_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query_data = query.data

    query.answer()  # ✅ REQUIRED to prevent spinner hang

    if query_data == "gen_mc":
        awaiting_name[user_id] = True
        context.bot.send_message(chat_id=user_id, text="📝 Please enter your full name for the medical certificate:")

    elif query_data == "continue_chat":
        context.bot.send_message(chat_id=user_id, text="💬 What would you like to ask about next?")

    elif query_data == "return_main":
        clear_user_session(user_id)
        show_main_menu(user_id, context.bot)



def clear_user_session(user_id: int):
    conversation_state.pop(user_id, None)
    user_symptom_message.pop(user_id, None)
    followup_context.pop(user_id, None)
    chat_history.pop(user_id, None)
    awaiting_name.pop(user_id, None)
    awaiting_nric.pop(user_id, None)
    temp_user_inputs.pop(user_id, None)

def suggest_rest_days(text: str) -> int:
    try:
        days = generate_rest_days_suggestion(text)
        return max(1, min(days, 14))  # Clamp to 1-14 days
    except Exception:
        return 1
