
####################################################################################################
### TELEGRAM SERVICE
####################################################################################################

import logging
import requests
from app.core.config import TIMEOUT
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self, bot_token: str, chat_id: str) -> None :
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, text: str) -> None :
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        response = requests.post(
            url=url,
            json={
                "chat_id": self.chat_id,
                "text": text,
            },
            timeout=TIMEOUT,
        )
        logger.info(f"TELEGRAM STATUS: {response.status_code}")
        logger.info(f"TELEGRAM BODY: {response.text}")
        response.raise_for_status()