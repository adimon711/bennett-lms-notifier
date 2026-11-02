import os
import json
import requests
from google import genai
from dotenv import load_dotenv

# Load environment variables from your local .env file
load_dotenv()

LMS_TOKEN = os.getenv("LMS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

STATE_FILE = "sent_notifications.json"

# Load previously sent notification IDs to prevent clutter
sent_ids = set()
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            sent_ids = set(json.load(f))
    except Exception:
        sent_ids = set()

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# 1. Authenticate with Moodle
site_info = requests.get(
    "https://lms.bennett.edu.in/webservice/rest/server.php", 
    params={"wstoken": LMS_TOKEN, "wsfunction": "core_webservice_get_site_info", "moodlewsrestformat": "json"}
).json()

user_id = site_info.get("userid")

if user_id:
    # 2. Fetch Notifications
    notification_params = {
        "wstoken": LMS_TOKEN, 
        "wsfunction": "message_popup_get_popup_notifications", 
        "moodlewsrestformat": "json", 
        "useridto": user_id
    }
    notifications = requests.get(
        "https://lms.bennett.edu.in/webservice/rest/server.php", 
        params=notification_params
    ).json().get('notifications', [])
    
    # 3. Filter for truly new notifications
    new_notifications = []
    for notif in notifications:
        notif_id = notif.get('id')
        if notif_id and notif_id not in sent_ids:
            new_notifications.append(notif)
    
    if new_notifications:
        # 4. Compile text for Gemini
        raw_text = ""
        for notif in new_notifications:
            raw_text += f"Subject: {notif.get('subject')}\nMessage: {notif.get('fullmessage', '')}\n---\n"
        
        # 5. Ask Gemini to read and summarize
        prompt = (
            "You are my personal assistant. Read these university LMS notifications. "
            "Filter out routine clutter, give me a concise bulleted summary of new assignments, "
            "and highlight any urgent deadlines in bold:\n\n" + raw_text
        )
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        
        # 6. Send the Summary to Discord
        payload = {
            "content": f"🎓 **Your Daily Bennett LMS Update**\n{response.text}"
        }
        requests.post(DISCORD_WEBHOOK, json=payload)
        
        # Save new IDs to prevent future duplicates
        for notif in new_notifications:
            if notif.get('id'):
                sent_ids.add(notif.get('id'))
        with open(STATE_FILE, "w") as f:
            json.dump(list(sent_ids), f)
            
        print("New notifications summary successfully sent to Discord!")
    else:
        print("No new notifications found. Staying quiet.")
else:
    print("Failed to authenticate with LMS.")