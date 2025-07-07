from utils.twitter_stream import twitter_loop
from utils.news_stream import news_loop
from utils.rl_agent import RLAgent
from utils.daily_report import generate_daily_report
import asyncio
from strategies.engine import start_engine

async def technical_loop():
    # Technical analysis loop
    while True:
        # TODO: implement
        await asyncio.sleep(60)

async def ml_loop():
    # ML model loop
    while True:
        # TODO: implement
        await asyncio.sleep(300)


async def engine_loop():
    """Loop for generating and executing signals."""
    while True:
        await start_engine()
        await asyncio.sleep(1)  # adjust interval as needed

async def agent_loop():
    # Agent adjustment loop
    while True:
        # TODO: implement
        await asyncio.sleep(600)


async def daily_report_loop():
    """Loop que envia relatório diário via Telegram a cada 24h"""
    while True:
        # espera até meia-noite UTC
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        # próximo dia 00:00 UTC
        next_run = datetime(now.year, now.month, now.day) + timedelta(days=1)
        delay = (next_run - now).total_seconds()
        await asyncio.sleep(delay)


async def rl_loop():
    """Loop que treina e avalia o agente de RL periodicamente."""
    agent = RLAgent(symbol=None)  # pode adaptar para múltiplos símbolos
    while True:
        # Treina o agente
        agent.train(episodes=100)
        # Espera um período (e.g., 6h) antes do próximo treino
        await asyncio.sleep(6 * 3600)
        send_daily_report()

def start_tasks():
    _task_list = []
    loop = asyncio.get_event_loop()
    _task_list.append(loop.create_task(technical_loop()))
    _task_list.append(loop.create_task(ml_loop()))
    _task_list.append(loop.create_task(agent_loop()))
    # Start engine
    loop.create_task(start_engine())
    return _task_list

async def cancel_tasks():
    for t in asyncio.all_tasks():
        t.cancel()
