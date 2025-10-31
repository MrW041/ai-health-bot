from flask import Flask, request
from deep_translator import GoogleTranslator
import requests

app = Flask(__name__)

# Rasa REST channel endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Default target language (change "hi" if you want another)
DEFAULT_TARGET_LANG = "hi"


def handle_twilio_message():
    """Main logic for handling incoming Twilio messages."""
    user_msg = request.form.get("Body") or ""
    user_id = request.form.get("From") or "default"

    # 1. Translate incoming → English
    translated_msg = GoogleTranslator(source="auto", target="en").translate(user_msg)

    # 2. Send to Rasa
    rasa_response = requests.post(
        RASA_URL, json={"sender": user_id, "message": translated_msg}
    ).json()

    # 3. Collect bot response (English)
    if rasa_response and "text" in rasa_response[0]:
        bot_reply_en = rasa_response[0]["text"]
    else:
        bot_reply_en = "Sorry, I didn't get that."

    # 4. Translate bot reply back → Hindi (or your target language)
    bot_reply_translated = GoogleTranslator(
        source="en", target=DEFAULT_TARGET_LANG
    ).translate(bot_reply_en)

    # Debug logs in console
    print("User:", user_msg)
    print("Translated to EN:", translated_msg)
    print("Bot EN:", bot_reply_en)
    print("Bot Translated:", bot_reply_translated)

    # 5. Send XML response back to Twilio
    response_xml = f"<Response><Message>{bot_reply_translated}</Message></Response>"
    return response_xml, 200, {"Content-Type": "application/xml"}


# Support multiple possible Twilio webhook routes
@app.route("/twilio", methods=["POST"])
def twilio_webhook():
    return handle_twilio_message()


@app.route("/webhooks/twilio/webhook", methods=["POST"])
def twilio_webhook_alias():
    return handle_twilio_message()


@app.route("/", methods=["POST"])
def root_webhook():
    return handle_twilio_message()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
