
####################################################################################################
### LLM SERVICES
####################################################################################################

from app.core import config
from app.clients.LLM_server_client import LLMClient
from app.tools import TOOLS_DESCRIPTIONS, TOOLS_REGISTRY

import json
import logging

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def run(self, user_message: str) -> str:
        messages = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        response = await self.llm_client.chat(messages=messages)

        return response["choices"][0]["message"]["content"]
    

class SplitterAgent:
    def __init__(self, llm_client: LLMClient, system_prompt: str | None = None):
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.messages = []
        if self.system_prompt is not None:
            self.messages = [{"role": "system", "content": self.system_prompt}]
    
    def clear_history(self):
        if self.system_prompt is not None :
            self.messages = [{"role": "system", "content": self.system_prompt}]
        else :
            self.messages = []

    async def run_one(self, user_message: str) -> str :

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        response = await self.llm_client.chat(
            messages=self.messages,
            model="qwen3.6:35b",
            temperature=config.TEMPERATURE,
            # tools=TOOLS_DESCRIPTIONS
        )

        return response
    
        assistant_message = response["choices"][0]["message"]

        self.messages.append(assistant_message)

        logger.info(f"messages list: \n{self.messages}")
        
        if assistant_message.get("tool_calls") is None :
            return assistant_message["content"]
        

    async def run(self, user_message: str) -> str :
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        for _ in range(config.MAX_TOOLS_ITERATIONS) :

            response = await self.llm_client.chat(
                messages=self.messages,
                model="qwen3.6:35b",
                temperature=config.TEMPERATURE,
                # tools=TOOLS_DESCRIPTIONS
            )

            assistant_message = response["choices"][0]["message"]

            self.messages.append(assistant_message)

            logger.info(f"messages list: \n{self.messages}")
            
            if assistant_message.get("tool_calls") is None :
                return assistant_message["content"]
            
            for tool_call in assistant_message["tool_calls"]:
                fn_name = tool_call["function"]["name"]
                fn_raw_args = tool_call["function"]["arguments"]
                try:
                    fn_args = json.loads(fn_raw_args)
                except json.JSONDecodeError as e:
                    pass
                fn = TOOLS_REGISTRY.get(fn_name)
                result = fn(**fn_args)

                logger.info(f"calling {fn_name}({fn_raw_args}) ... {result}")

                self.messages.append({
                    "role": "tool",
                    "name": fn_name,
                    "content": result,
                    "tool_call_id": tool_call.get("id")
                })

        else :
            return (
                f"Failed to complete the request after {config.MAX_TOOLS_ITERATIONS} iterations."
                "\nToo many steps required."
            )