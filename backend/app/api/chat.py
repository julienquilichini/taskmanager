from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.telegram import TelegramService
from app.core import config


router = APIRouter()
jarvis_bot = TelegramService(bot_token=config.TELEGRAM_JS_BOT_TOKEN, chat_id=config.TELEGRAM_CHAT_ID)


@router.post("/chat")
def chat_response(request: ChatRequest) -> ChatResponse :
    user_prompt = request.message
    jarvis_bot.send_message(user_prompt)
    return {"answer": f"Jarvis a envoyé : {user_prompt}"}
