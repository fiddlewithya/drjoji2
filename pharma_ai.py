# pharma_ai.py
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_symptom_response(user_combined_input: str, force_type: str = "symptom"):
    try:
        user_lines = user_combined_input.strip().split("User's question:")
        user_question = user_lines[-1].strip() if len(user_lines) > 1 else user_combined_input.strip()

        if force_type == "medication":
            system_prompt = (
                "You are a professional pharmacy assistant. Respond in this format using emojis and Markdown:\n\n"
                "💊 **What It Is**\n"
                "📝 **How to Use**\n"
                "⚠️ **Precautions**\n"
                "🚨 **When to Stop / Side Effects**\n"
                "📌 **Disclaimer**"
            )
        else:
            system_prompt = (
                "You are a helpful and professional pharmacy assistant. Respond to symptoms in this structured format with emojis and Markdown:\n\n"
                "🔍 **Possible Causes**\n"
                "💊 **Immediate Recommendations**\n"
                "🚨 **Red Flags**\n"
                "🩺 **When to See a Doctor**\n"
                "📌 **Disclaimer**"
            )

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_combined_input}
            ],
            temperature=0.6,
            max_tokens=600,
        )

        reply = response.choices[0].message.content
        return reply, force_type

    except Exception as e:
        print("❌ OpenAI error:", str(e))
        return "❌ AI is currently unavailable. Please try again later or speak to a pharmacist.", "error"

def generate_free_response(user_id: int, new_input: str, history: list = None) -> str:
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful and professional pharmacist chatbot named Dr.Joji. "
                    "You only respond to questions related to health, medications, symptoms, minor ailments, supplements, or pharmacy-related topics. "
                    "If the user asks about unrelated topics like electronics, celebrities, politics, or general tech, politely redirect them and say: "
                    "'I'm here to assist with medical or pharmacy-related concerns. Let me know how I can help with any symptoms or health questions you may have.'"
                )
            }
        ]

        if history:
            messages += history[-6:]
        messages.append({"role": "user", "content": new_input})

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Free response error:", e)
        return "❌ Sorry, I couldn’t process that. Please speak to a pharmacist if you need further help."

def generate_rest_days_suggestion(ailment_text: str) -> int:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced medical assistant. "
                        "Based on the patient's condition, reply ONLY with a number between 1 and 14 representing the recommended medical rest days. "
                        "Do not include any words, just the number."
                    )
                },
                {"role": "user", "content": f"Patient condition: {ailment_text}"}
            ],
            temperature=0,
            max_tokens=5,
        )
        reply = response.choices[0].message.content.strip()
        days = int(reply)
        return days
    except Exception as e:
        print("Rest day AI error:", str(e))
        return 1  # Safe fallback
