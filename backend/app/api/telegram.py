from fastapi import APIRouter, Request, BackgroundTasks

from app.clients.LLM_server_client import LLMClient
from app.services.task_splitter import SplitterAgent
from app.services.telegram import TelegramService

from app.core import config
from app.core import agents_instructions

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(request: Request, background_task: BackgroundTasks) -> dict[str, str]:
    update = await request.json()

    message = update.get("message")
    if not message:
        return {"status": "ignored"}

    text = message.get("text")
    chat_id = message.get("chat", {}).get("id")

    print(f"Received new message :{text}")
    print(f"{str(message)}")

    if not text or not chat_id:
        return {"status": "ignored"}

    background_task.add_task(handle_telegram_message, text, chat_id)
    
    return {"status": "accepted"}

@router.post("/callback")
async def callback_server_handling(request: Request) -> None :

    response = await request.json()
    logger.info(response)
    
    assistant_message = response["choices"][0]["message"]
    logger.info(f"Assistant message : {assistant_message}")

    telegram_service = TelegramService(
        bot_token=config.TELEGRAM_JS_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID
    )

    telegram_service.send_message(
        text=assistant_message["content"]
    )


async def handle_telegram_message(text: str, chat_id: str) -> None:

    llm_client = LLMClient(
        client_url="https://s2.quilichini.cloud/smallm", 
        auth_token=config.LLM_CLIENT_TOKEN
    )

    splitter_agent = SplitterAgent(
        llm_client=llm_client, 
        system_prompt=agents_instructions.AGENT_1_PROMPT
    )

    telegram_service = TelegramService(
        bot_token=config.TELEGRAM_JS_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID
    )

    telegram_service.send_message(
        text="Thinking ..."
    )

    response = await splitter_agent.run_one(user_message=text)
    logger.info(response)

