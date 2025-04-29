from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("👨‍⚕️ Talk to Dr.Joji ", callback_data='ailments')],
        [InlineKeyboardButton("💊 Ask About Medications & Devices", callback_data='products')],
    ]
    return InlineKeyboardMarkup(keyboard)

def return_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Return to Main Menu", callback_data='return_main')]
    ])

def followup_options_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Continue Consultation", callback_data="continue_chat")
        ],
        [
            InlineKeyboardButton("🏠 Return to Main Menu", callback_data="return_main")
        ]
    ])


def generate_mc_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Generate Medical Certificate", callback_data="gen_mc")
        ],
        [
            InlineKeyboardButton("🔄 Continue Consultation", callback_data="continue_chat")
        ],
        [
            InlineKeyboardButton("🏠 Return to Main Menu", callback_data="return_main")
        ]
    ])


def tnc_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Agree", callback_data="agree"),
            InlineKeyboardButton("❌ Disagree", callback_data="disagree"),
        ]
    ])