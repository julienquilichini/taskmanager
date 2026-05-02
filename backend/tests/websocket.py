import asyncio
import json

import websockets


WS_URL = "wss://s0.quilichini.cloud/call/in/ws"


async def main() -> None:
    user_instruction = input("Instruction > ").strip()

    if not user_instruction:
        print("No instruction.")
        return

    async with websockets.connect(WS_URL) as ws:
        print("connected")

        await ws.send(json.dumps({
            "type": "setup",
            "callSid": "CA_TEST",
            "from": "+33600000000",
        }))

        await ws.send(json.dumps({
            "type": "prompt",
            "voicePrompt": user_instruction,
            "last": True,
        }))

        while True:
            msg = await ws.recv()
            print("recv:", msg)


if __name__ == "__main__":
    asyncio.run(main())