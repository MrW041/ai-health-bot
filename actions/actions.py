#now
import json
import os
import re
from typing import Any, Text, Dict, List

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

ACTION_FILE_PATH = os.path.dirname(os.path.abspath(__file__))


DISEASES_JSON_PATH = os.path.join(ACTION_FILE_PATH, "..", "_DISEASES.json") #.json only
OUTBREAKS_CSV_PATH = os.path.join(ACTION_FILE_PATH, "..", "odisha_cases.csv")# .csv only

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'[\s\-_()]', '', text.lower())

class ActionFindAnswer(Action):
    def name(self) -> Text:
        return "action_find_answer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            with open(DISEASES_JSON_PATH, 'r', encoding='utf-8') as f:
                disease_db = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text=f"Error: The file {DISEASES_JSON_PATH} was not found. Please check the filename in actions.py.")
            return []

        disease_slot = tracker.get_slot("disease")
        if not disease_slot:
            dispatcher.utter_message(response="utter_ask_disease")
            return []

        normalized_disease_slot = normalize_text(disease_slot)
        intent_name = ""
        for event in reversed(tracker.events):
            if event.get("event") == "user":
                intent = event.get("parse_data", {}).get("intent", {}).get("name", "")
                if intent.startswith("ask_"):
                    intent_name = intent
                    break
        
        # --- FIX FOR BUG #4 ---
        # If the user just says a disease name (intent='inform'), we don't know the topic.
        if not intent_name or tracker.latest_message['intent'].get('name') == 'inform':
            dispatcher.utter_message(text=f"What would you like to know about {disease_slot}? You can ask about symptoms, prevention, risks, etc.")
            return []

        topic_map = {
            'ask_about': 'about',
            'ask_symptoms': 'symptoms',
            'ask_prevention': 'prevention',
            'ask_transmission': 'transmission',
            'ask_vaccine': 'vaccine',
            'ask_risk_factors': 'risk_factors',
            'ask_misconceptions': 'misconceptions'
        }
        topic = topic_map.get(intent_name)
        response = None
        found_disease = None
        for record in disease_db:
            normalized_name = normalize_text(record.get('disease_name', ''))
            normalized_id = normalize_text(record.get('disease_id', ''))
            if normalized_disease_slot == normalized_name or normalized_disease_slot == normalized_id:
                found_disease = record
                break
        if found_disease:
            info = found_disease['data'].get(topic)
            if info:
                display_topic = "overview" if intent_name == 'ask_about' else topic
                response = f"Here is an {display_topic} of {found_disease['disease_name']}:\n\n{info}"
            else:
                response = f"I'm sorry, I don't have information on the {topic} for {found_disease['disease_name']}."
        else:
            response = f"I'm sorry, I could not find any information for the disease '{disease_slot}'. Please check the spelling."
        dispatcher.utter_message(text=response)
        return []

# ActionFindCure and ActionCheckOutbreaks classes remain the same
class ActionFindCure(Action):
    def name(self) -> Text:
        return "action_find_cure"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_medical_advice_disclaimer")
        return []

class ActionCheckOutbreaks(Action):
    def name(self) -> Text:
        return "action_check_outbreaks"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        if not location:
            dispatcher.utter_message(text="Please provide a district in Odisha to check for outbreaks.")
            return []
        try:
            df = pd.read_csv(OUTBREAKS_CSV_PATH)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: The odisha_cases.csv file was not found.")
            return []
        filtered_df = df[(df['Name of State/UT'] == 'Odisha') & (df['Name of District'].str.lower() == location.lower())]
        if not filtered_df.empty:
            response_text = f"Found recent outbreak alerts for {location.title()}, Odisha:\n\n"
            for index, row in filtered_df.iterrows():
                response_text += (f" disease: **{row['Disease/Illness']}**\n No. of Cases: **{row['No. of Cases']}**\n No. of Deaths: **{row['No. of Deaths']}**\n Status: **{row['Current Status']}**\n Reported on: {row['Date of Reporting']}\n---\n")
        else:
            response_text = f"Good news! There are no recently reported disease outbreaks for {location.title()} in Odisha based on my data."
        dispatcher.utter_message(text=response_text)
        return []
