import os

import httpx
from fastapi import APIRouter, Request, HTTPException, Header
from app.core import config

router = APIRouter()

API_TOKEN = config.LLM_CLIENT_TOKEN
OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"


@router.post("/smallm")
async def chat(request: Request, authorization: str | None = Header(default=None)):

    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()

    async with httpx.AsyncClient(timeout=900) as client:
        response = await client.post(
            OLLAMA_URL,
            json=body,
        )

    return response.json()