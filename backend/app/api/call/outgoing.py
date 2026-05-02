# /app/api/call/webhook_in.py

####################################################################################################
### IMPORTS
####################################################################################################
import json

from fastapi import APIRouter, Request
from fastapi.responses import Response
from fastapi import WebSocket, WebSocketDisconnect

from twilio.twiml.voice_response import VoiceResponse

from app.core import config
from app.agents import BookingAgent

from app.db.engine import SessionLocal
from app.db.repositories.outbound_call_repository import OutboundCallRepository

router = APIRouter(prefix="/call", tags=["outgoing_call"])


####################################################################################################
### WEBHOOK
####################################################################################################

@router.post("/out")
async def outgoing_call_webhook(request: Request):
    """ Twilio webhook for outgoing calls -> called by twilio then transfered to a websocket"""
    form = await request.form()

    call_sid = form.get("CallSid")
    from_number = form.get("From")
    to_number = form.get("To")
    answered_by = form.get("AnsweredBy")

    print(f"Answered by: {answered_by}")
    if answered_by in {"machine_start", "machine_end", "fax"}:
        response = VoiceResponse()
        response.hangup()
        return Response(content=str(response), media_type="application/xml")

    print("=== Outgoing Call Answered ===")
    print(f"CallSid: {call_sid}")
    print(f"From: {from_number}")
    print(f"To: {to_number}")
    print("=====================")

    with SessionLocal() as db:
        repo = OutboundCallRepository(db)
        call_data = repo.get_by_call_sid(call_sid)
    greeting = call_data.greeting if call_data else "Allo"

    response = VoiceResponse()
    connect = response.connect()
    connect.conversation_relay(
        url=f"wss://{config.CALL_SERVER}/call/out/ws",
        # welcome_greeting=greeting,
        language="fr-FR",
        interruptible="none",
        debug="debugging speaker-events",
    )

    print(f"[CALL OUT] Response: {response}", flush=True)

    return Response(content=str(response), media_type="application/xml")


####################################################################################################
### WEBSOCKET
####################################################################################################

@router.websocket("/out/ws")
async def incoming_ws_connect(websocket: WebSocket):
    """
    Twilio ConversationRelay WebSocket.
    Basic debug version: prints all incoming events and prompt text.
    """
    await websocket.accept()
    print("\n[WS] connected to ConversationRelay\n", flush=True)

    booking_agent: BookingAgent = websocket.app.state.booking_agent

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

                # await websocket.send_text(json.dumps({
                #     "type": "text",
                #     "token": "Allo",
                #     "last": True,
                # }))     
                with SessionLocal() as db:
                    repo = OutboundCallRepository(db)
                    call_data = repo.get_by_call_sid(call_sid)

                if call_data :
                    booking_agent.reset_instructions(instructions=call_data.instructions, context=call_data.context or "")       
    
                print("\n[SETUP]", flush=True)
                print(f"call_sid={call_sid}", flush=True)
                print(f"from={from_number}", flush=True)

            elif msg_type == "prompt":
                user_text = msg.get("voicePrompt", "")
                is_last = msg.get("last", False)

                print("\n[PROMPT]", flush=True)
                print(f"[USER]: {user_text}", flush=True)

                if is_last:

                    agent_reply = await booking_agent.reply(user_text)

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