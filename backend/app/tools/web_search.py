from tavily import TavilyClient, AsyncTavilyClient
from app.core import config
import requests
import json

def search_web(query: str):

    response = requests.post(
        url="https://api.tavily.com/search",
        headers={
            "Content-Type": "application/json",
            "Authorization": F"Bearer {config.TAVILY_API_KEY}"
        },
        json={
            "query": f"{query}"
        }
    )
    response.raise_for_status()

    return json.dumps(response.json())





