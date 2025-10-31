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

##  How It Works

This bot uses Rasa's NLU to understand user messages and Rasa Core to manage the conversation.
* **Custom Actions (`actions.py`):** Handle all the complex logic, such as:
    * Querying the `_DISEASES.json` files for information.
    * Performing the live web scrape for outbreak data.
* **Twilio Connector:** Uses the built-in Rasa connector to send and receive messages from the Twilio WhatsApp API.
* **Ngrok (for Development):** Exposes the local Rasa server to the public internet, allowing Twilio's webhooks to connect to your development machine.

## Setup & Installation

Follow these steps to get your local development environment set up.

**1. Clone the Repository**
```bash
git clone [https://github.com/MrW041/ai-health-bot.git](https://github.com/MrW041/ai-health-bot.git)

**2. Create a virtual environment**
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

**Note: Install the RASA inside the .venv**

**3. Train the RASA Model**
Note: Train the model after you have used to replace the files with the files given in the repository.
# run in the terminal:
      >> rasa train

**4. Adding Credentials**
# Open the credentials.yml in the venv where the project files are placed.

# Add the following in the last of your credentials.yml:
      twilio:
        account_sid: "YOUR_TWILIO_ACCOUNT_SID_HERE"
        auth_token: "YOUR_TWILIO_AUTH_TOKEN_HERE"
        twilio_number: "whatsapp:+1234567890"  # Your Twilio WhatsApp Number
  Note: Make sure to change the account_sid, auth_token, twilio_number.

**5. Running The Bot**
# Running the bot Locally:
    run:
        >> rasa run actions
        >> rasa shell
# Running the bot through WhatsApp:

'''open 2 terminals for this process'''
terminal_1:
  >> rasa run actions
terminal_2:
  >> ngrok http 5005

Note: Make sure the Twilio is connected successfully to the ngrok generated link
if not:
    1. After running Ngrok, it will give you a Forwarding URL that looks like https://abcdef123.ngrok.io. Copy this HTTPS URL.

    2. Go to your Twilio Dashboard > Messaging > Settings > WhatsApp Sandbox Settings.

    3. In the field labeled "WHEN A MESSAGE COMES IN", paste your Ngrok URL and add /webhooks/twilio/webhook to the end of it.

    4. The final URL should look like this: https://abcdef123.ngrok.io/webhooks/twilio/webhook

    5. Set the method to HTTP POST.

    6. Click Save.


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

