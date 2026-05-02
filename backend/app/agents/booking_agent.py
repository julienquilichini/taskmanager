from app.tools import TOOLS_DESCRIPTIONS, TOOLS_REGISTRY
from app.core import config

from mistralai.client import Mistral

import logging
import json

logger = logging.getLogger(__name__)

class BookingAgent:
    def __init__(self, system_prompt: str | None = None) -> None :
        self.client = Mistral(api_key=config.MISTRAL_API_KEY)
        self.system_prompt = system_prompt
        self.messages = []
        if system_prompt is not None :
            self.messages = [{
                "role": "system", 
                "content": self.system_prompt
            }]

    def reset(self) -> None :
        if self.system_prompt is not None :
            self.messages = [{
                "role": "system", 
                "content": self.system_prompt
            }]
        else :
            self.messages = []

    def reset_instructions(self, instructions: str = "", context: str = "") -> None :
        self.messages = [{
            "role": "system", 
            "content": f"""{self.system_prompt}\n\n[SPECIFIC CALL INSTRUCTIONS]\n{instructions}\n\n[CONTEXT]\n{context}"""
        }]

    async def reply(self, user_prompt: str) -> str:

        self.messages.append({
            "role": "user",
            "content": user_prompt
        })        

        for _ in range(config.MAX_TOOLS_ITERATIONS):

            try :
                response = await self.client.chat.complete_async(
                    model="mistral-small-latest",
                    messages=self.messages,
                    temperature=config.TEMPERATURE,
                    # tool_choice="auto",
                    # tools=TOOLS_DESCRIPTIONS,
                )
                agent_message = response.choices[0].message

            except Exception as e :
                logger.error(f"[ERROR] something wrong happened with the Mistral API: {str(e)}")
                raise
            
            self.messages.append(agent_message)
            
            if not agent_message.tool_calls :
                return agent_message.content

            for tool_call in agent_message.tool_calls :

                fn_name = tool_call.function.name
                fn_raw_args = tool_call.function.arguments
                
                fn = TOOLS_REGISTRY.get(fn_name)

                if fn is None :
                    logger.error(f"Unknown tool {fn_name}")
                    result = f"Unknown tool {fn_name}"
                else :
                    try:
                        fn_args = json.loads(fn_raw_args)
                        result = fn(**fn_args)
                    except Exception as e :
                        logger.error(f"[ERROR] {str(e)}")
                        result = f"Tool error: {str(e)}"

                self.messages.append({
                    "role": "tool",
                    "name": fn_name,
                    "content": result,
                    "tool_call_id": tool_call.id
                })

                logger.info(f"[TOOL]: Calling {fn_name}({fn_args}) -> {result}")

        else:

            return (
                "Unable to perform the operation within the iterations limit." \
                "Too many steps required."
            )