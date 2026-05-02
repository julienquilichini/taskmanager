from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.telegram import router as telegram_router
from app.api.llm_planner import router as llm_planner_router
from app.api.call.incoming import router as incoming_router
from app.api.call.outgoing import router as outgoing_router

from app.db.engine import Base, engine
from app.db import models

from app.agents.voice_agent import VoiceAgent
from app.agents.booking_agent import BookingAgent

from app.core import agents_instructions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Starting server ...")

    logger.info("Loading agents ...")
    app.state.voice_agent = VoiceAgent(system_prompt=agents_instructions.VOICE_AGENT_SP)
    app.state.booking_agent = BookingAgent(system_prompt=agents_instructions.BOOKING_AGENT_SP)
    logger.info("Agents loaded")

    logger.info("Starting database engine...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready")

    logger.info("Server ready 🟢")

    yield

    logger.info("Stopping server...")
    logger.info("Server stopped 🛑")

app = FastAPI(title="Agentic App", lifespan=lifespan)

app.include_router(telegram_router)
app.include_router(llm_planner_router)
app.include_router(incoming_router)
app.include_router(outgoing_router)

@app.get("/")
def health():
    return {"status": "ok"}