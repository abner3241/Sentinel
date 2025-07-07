import asyncio
from services.news_client import get_headlines
from handlers.telegram import bot

async def news_loop(keywords, interval_sec=300):
    """Loop que busca notícias e envia alertas no Telegram."""
    while True:
        headlines = get_headlines(keywords)
        for hl in headlines:
            await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=f"📰 {hl}")
        await asyncio.sleep(interval_sec)
