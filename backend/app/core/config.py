
####################################################################################################
### IMPORTS
####################################################################################################

import os
from pathlib import Path

from dotenv import load_dotenv

# Charge backend/.env quel que soit le cwd
# (ce fichier est à backend/app/core/config.py -> on remonte de 3 niveaux)
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


####################################################################################################
### API_KEYS
####################################################################################################

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LLM_CLIENT_TOKEN = os.getenv("LLM_CLIENT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


####################################################################################################
### SERVER URLS
####################################################################################################

SERVER_0 = os.getenv("SERVER_0")
SERVER_1 = os.getenv("SERVER_1")
SERVER_2 = os.getenv("SERVER_2")

CALL_SERVER = SERVER_0
CALL_SERVER_URL = f"https://{SERVER_0}"


####################################################################################################
### TELEGRAM
####################################################################################################

TELEGRAM_JS_BOT_TOKEN = os.getenv("TELEGRAM_JS_BOT_TOKEN")
TELEGRAM_VT_BOT_TOKEN = os.getenv("TELEGRAM_VT_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


####################################################################################################
### TWILIO
####################################################################################################

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ALLOWED_NUMBERS = os.getenv("ALLOWED_NUMBERS")


####################################################################################################
### GOOGLE CALENDAR
####################################################################################################

GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    str(BACKEND_DIR / "secrets" / "calendar_credentials.json"),
)
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")
GOOGLE_CALENDAR_TIMEZONE = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "Europe/Paris")


####################################################################################################
### AGENT CONST
####################################################################################################

TIMEOUT = 10
TEMPERATURE = 0.1
MAX_TOOLS_ITERATIONS = 10


