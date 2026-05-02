import httpx


class LLMClient:
    """LLM Client exposed via a server endpoint."""
    def __init__(self, client_url: str, auth_token: str):
        self.client_url = client_url
        self.token = auth_token

    async def chat(self, messages: list[dict], model: str = "qwen2.5:3b-instruct", temperature: float = 0.1, tools: list[dict] | None = None) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        async with httpx.AsyncClient(timeout=900) as client:
            response = await client.post(
                self.client_url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        response.raise_for_status()
        return response.json()