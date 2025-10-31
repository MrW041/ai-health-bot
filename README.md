# RASA Health ChatBot

A comprehensive health-focused chatbot built with Rasa. It provides detailed information on various diseases, handles natural language queries, and can even fetch real-time outbreak data for specific regions.

The bot is designed to be fully interactive via **WhatsApp** using the Twilio API.

## Key Features

* **Detailed Disease Info:** Provides information on symptoms, prevention, transmission, vaccines, risk factors, and common misconceptions.
* **Natural Language:** Understands complex user questions, recognizes alternate/local disease names, and is resilient to small typos.
* **Verified Sources:** Provides a source link for all medical information to ensure trust and accuracy.
* **Live Outbreak Data:** Scrapes the latest outbreak information from the official [IDSP website](https://idsp.mohfw.gov.in/index4.php?lang=1&level=0&linkid=406&lid=3689).
* **Region-Specific:** The outbreak feature is currently configured to fetch data for **Odisha, India**, but the scraper can be customized.
* **WhatsApp Ready:** Built from the ground up to connect to WhatsApp via Twilio, allowing users to interact from their favorite messaging app.

## How It Works

This bot uses Rasa's NLU to understand user messages and Rasa Core to manage the conversation.
* **Custom Actions (`actions.py`):** Handle all the complex logic, such as:
    * Querying the `_DISEASES.json` files for information.
    * Performing the live web scrape for outbreak data.
* **Twilio Connector:** Uses the built-in Rasa connector to send and receive messages from the Twilio WhatsApp API.
* **Ngrok (for Development):** Exposes the local Rasa server to the public internet, allowing Twilio's webhooks to connect to your development machine.

---

# Step-by-Step Setup Guide

Follow this guide in exact order to get your bot running locally and connected to WhatsApp.

---

### 1. Clone the Repository
```bash
git clone https://github.com/MrW041/ai-health-bot.git
cd ai-health-bot
```

---

### 2. Create and Activate Virtual Environment
```bash
# For Windows
python -m venv venv
.
env\Scripts ctivate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

> **Note:** Install Rasa inside this virtual environment (`venv`).

---

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```
If there’s no `requirements.txt`, run:
```bash
pip install rasa rasa-sdk
```

---

### 4. Train the RASA Model
Replace any placeholder files if needed, then train:
```bash
rasa train
```

---

### 5. Add Twilio Credentials
Open the file `credentials.yml` in your project directory (inside `venv`).

Add this at the bottom:
```yaml
twilio:
  account_sid: "YOUR_TWILIO_ACCOUNT_SID_HERE"
  auth_token: "YOUR_TWILIO_AUTH_TOKEN_HERE"
  twilio_number: "whatsapp:+1234567890"  # Your Twilio WhatsApp Number
```

> Make sure to replace the credentials with your real Twilio details.

---

### 6. (Optional) Set Environment Variables
Instead of saving secrets in `credentials.yml`, you can export them as environment variables:
```bash
export TWILIO_ACCOUNT_SID="YOUR_TWILIO_ACCOUNT_SID_HERE"
export TWILIO_AUTH_TOKEN="YOUR_TWILIO_AUTH_TOKEN_HERE"
export TWILIO_NUMBER="whatsapp:+1234567890"
```

---

### 7. Run the Bot Locally
Open **two terminals**:

**Terminal 1:**
```bash
rasa run actions
```

**Terminal 2:**
```bash
rasa shell
```

This lets you chat with the bot locally before connecting to WhatsApp.

---

### 8. Connect to WhatsApp (via Twilio + Ngrok)

**Step 1:** Run Ngrok to expose your local Rasa server.
```bash
ngrok http 5005
```

**Step 2:** Copy the HTTPS forwarding URL from the Ngrok output, e.g.:
```
https://abcdef123.ngrok.io
```

**Step 3:** Go to your **Twilio Dashboard → Messaging → Settings → WhatsApp Sandbox Settings.**

**Step 4:** In the field “WHEN A MESSAGE COMES IN”, paste:
```
https://abcdef123.ngrok.io/webhooks/twilio/webhook
```

**Step 5:** Set the method to `HTTP POST` and click **Save**.

---

### 9. Start Full WhatsApp Connection
Open **two terminals** again.

**Terminal 1:**
```bash
rasa run actions
```

**Terminal 2:**
```bash
rasa run --enable-api
```

Keep Ngrok running in a separate terminal.  
Now send a WhatsApp message to your Twilio Sandbox number — the bot should reply.

---

### 10. Debug Checklist
If WhatsApp messages don’t reach the bot:
- Ensure both `rasa run` and `rasa run actions` are active.
- Verify Ngrok is running and URL is pasted correctly in Twilio.
- Check Twilio logs for webhook errors.
- Confirm Rasa server is on port 5005.

---

## 🚧 Project Roadmap

This project is still in development. Future plans and features under consideration include:

* **Language Translator:** Implementing a translation module to support multiple languages.
* **Expanded Knowledge Base:** Adding more diseases and health topics.
* **Deployment:** Moving from Ngrok to a more permanent hosting solution.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

## 👤 Author & Acknowledgments

* **Author:** [MrW041](https://github.com/MrW041)
* **Acknowledgments:**
    * This bot was built using the amazing open-source [Rasa](https://rasa.com/) framework.
    * Live outbreak data is sourced from the [IDSP, Ministry of Health & Family Welfare, India](https://idsp.mohfw.gov.in/index4.php?lang=1&level=0&linkid=406&lid=3689).
