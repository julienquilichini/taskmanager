
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
### AGENT CONST
####################################################################################################

SERVER_0_URL = os.getenv("SERVER_0_URL")
SERVER_1_URL = os.getenv("SERVER_1_URL")
SERVER_2_URL = os.getenv("SERVER_2_URL")


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
### AGENT CONST
####################################################################################################

TIMEOUT = 10
TEMPERATURE = 0.1
MAX_TOOLS_ITERATIONS = 10


