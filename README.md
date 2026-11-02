# Bennett LMS Discord Notifier 🎓🤖

An automated Python utility that connects to Bennett University's Moodle LMS REST API, filters out routine clutter, uses **Google Gemini (Gemini 3.5 Flash)** to summarize new assignments and urgent deadlines, and pushes the clean updates directly to a **Discord channel** via Webhook.

---

## Features ✨
* **API Integration:** Connects directly with Bennett LMS to fetch popup notifications.
* **Smart Filtering & AI Summary:** Uses Gemini AI to cut through notification clutter and highlight important academic updates and deadlines.
* **Duplicate Prevention:** Tracks sent notifications locally using a `sent_notifications.json` state tracker to prevent spamming your Discord server.
* **Fully Automated:** Can be scheduled via Windows Task Scheduler to run periodically in the background.
* **Security First:** Utilizes `python-dotenv` to ensure your sensitive LMS tokens and API keys never get hardcoded or leaked to GitHub.

---

## Tech Stack 🛠️
* **Python** (`requests`, `google-genai`, `python-dotenv`)
* **Bennett University Moodle LMS REST API**
* **Google Gemini API** (Gemini 3.5 Flash model)
* **Discord Webhooks**

---

## Setup & Installation 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/adimon711/bennett-lms-notifier.git
cd bennett-lms-notifier
