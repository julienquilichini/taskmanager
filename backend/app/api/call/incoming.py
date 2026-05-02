# /app/api/call/webhook_in.py

####################################################################################################
### IMPORTS
####################################################################################################
import json, asyncio

from fastapi import APIRouter, Request
from fastapi.responses import Response
from fastapi import WebSocket, WebSocketDisconnect

from twilio.twiml.voice_response import VoiceResponse

from app.core import config

router = APIRouter(prefix="/call", tags=["incoming_call"])


####################################################################################################
### WEBHOOK
####################################################################################################

@router.post("/in")
async def accept_call(request: Request):
    """webhook for twilio API audio calls -> if accepted, the call continues on ws (/call/in/ws)"""
    form = await request.form()

    call_sid = form.get("CallSid")
    from_number = form.get("From")

    print("=== Incoming Call ===")
    print(f"CallSid: {call_sid}")
    print(f"From: {from_number}")
    print("=====================")

    response = VoiceResponse()

    if not from_number in config.ALLOWED_NUMBERS:
        response.say("Bonjour, vous n'êtes pas autorisé à appeler.", language="fr-FR")
        return Response(content=str(response), media_type="application/xml")
    
    connect = response.connect()
    connect.conversation_relay(
        url="wss://s0.quilichini.cloud/call/in/ws",
        # welcome_greeting="Bonjour, quelles sont les instructions ?",
        language="fr-FR",
        interruptible="none",
        debug="debugging speaker-events",
    )

    print(f"[CALL IN] Response: {response}")
    return Response(content=str(response), media_type="application/xml")


####################################################################################################
### WEBSOCKET
####################################################################################################

@router.websocket("/in/ws")
async def incoming_ws_connect(websocket: WebSocket):
    """
    Twilio ConversationRelay WebSocket.
    Basic debug version: prints all incoming events and prompt text.
    """
    await websocket.accept()
    print("\n[WS] connected to ConversationRelay\n", flush=True)

    voice_agent = websocket.app.state.voice_agent

    call_sid = None
    from_number = None

    try:
        while True:
            raw_text = await websocket.receive_text()

            try:
                msg = json.loads(raw_text)
            except json.JSONDecodeError:
                print(f"[WS] non-JSON message: {raw_text}", flush=True)
                continue

            msg_type = msg.get("type")

            if msg_type == "setup":
                call_sid = msg.get("callSid")
                from_number = msg.get("from")

                await websocket.send_text(json.dumps({
                    "type": "text",
                    "token": "Bonjour, quelles sont les instructions ?",
                    "last": True,
                }))

                print("\n[SETUP]", flush=True)
                print(f"call_sid={call_sid}", flush=True)
                print(f"from={from_number}", flush=True)

            elif msg_type == "prompt":
                user_text = msg.get("voicePrompt", "")
                is_last = msg.get("last", False)

                print("\n[PROMPT]", flush=True)
                print(f"[USER]: {user_text}", flush=True)

                if is_last:
                    agent_reply = await voice_agent.reply(user_text)
                    print(f"\n[AGENT]: {agent_reply}")
                    await websocket.send_text(json.dumps({
                                "type": "text",
                                "token": agent_reply,
                                "last": True,
                    }))
                    if "au revoir" in agent_reply.lower():
                        await websocket.send_text(json.dumps({
                            "type": "end",
                        }))

            elif msg_type == "interrupt":
                print("\n[INTERRUPT]", flush=True)
                print(msg, flush=True)

            elif msg_type == "error":
                print("\n[ERROR]", flush=True)
                print(msg, flush=True)

    except WebSocketDisconnect:
        print("\n[WS] disconnected", flush=True)
        print(f"call_sid={call_sid}", flush=True)
        print(f"from={from_number}", flush=True)