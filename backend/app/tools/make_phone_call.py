# app/tools/make_phone_call.py

from app.clients.phone_clients.twilio_client import TwilioClient
from app.core import config

from app.db.engine import SessionLocal
from app.db.repositories.outbound_call_repository import OutboundCallRepository

import json

def make_phone_call(phone_number: str, instructions: str, context: str | None = None, greeting: str | None = None) -> str:
    """
    Tool called by the agent to start an outbound phone call.
    The actual voice conversation will be handled by /call/out and /call/out/ws.
    """

    twilio_client = TwilioClient(
        account_sid=config.TWILIO_ACCOUNT_SID,
        auth_token=config.TWILIO_AUTH_TOKEN,
        from_number=config.TWILIO_PHONE_NUMBER,
    )

    # call = twilio_client.create_call_with_machine_detection(
    #     to_number=phone_number,
    #     webhook_url=f"{config.CALL_SERVER_URL}/call/out",
    # )

    call = twilio_client.create_call(
        to_number=phone_number,
        webhook_url=f"{config.CALL_SERVER_URL}/call/out",
    )

    with SessionLocal() as db:
        repo = OutboundCallRepository(db)
        repo.create(
            call_sid=call.sid,
            phone_number=phone_number,
            instructions=instructions,
            context=context,
            greeting=greeting or "Allo",
        )
    print("SID: ", call.sid)

    return json.dumps({"output": "Process successful, the call will be made shortly. Consider it done, no need to call the tool again."})