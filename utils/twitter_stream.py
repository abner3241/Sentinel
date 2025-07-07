import asyncio
import os
import tweepy
from handlers.telegram import bot

# Twitter API credentials from environment
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

async def twitter_loop(keywords, interval_sec=300):
    """Loop que busca tweets recentes via Twitter API v2 e envia ao Telegram."""
    if not TWITTER_BEARER_TOKEN:
        return
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    last_id = None
    while True:
        # Search recent tweets
        query = ' OR '.join(keywords) + ' -is:retweet lang:en'
        tweets = client.search_recent_tweets(query=query, since_id=last_id, max_results=5)
        if tweets.data:
            for tweet in tweets.data:
                text = tweet.text
                await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=f"🐦 {text}")
            last_id = tweets.data[0].id
        await asyncio.sleep(interval_sec)
