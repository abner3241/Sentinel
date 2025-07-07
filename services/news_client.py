
import httpx
from utils.config_manager import ConfigManager

class NewsClient:
    def __init__(self):
        self.api_key = ConfigManager.get("NEWS_API_KEY")

    async def fetch_news(self, query: str, page_size: int = 10):
        url = "https://newsapi.org/v2/everything"
        params = {"q": query, "pageSize": page_size, "apiKey": self.api_key}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            data = resp.json()
        return data.get("articles", [])
