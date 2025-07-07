import asyncio
from datetime import datetime, timedelta
from utils.twitter_stream import twitter_loop
from utils.news_stream import news_loop
from utils.rl_agent import RLAgent
from utils.daily_report import generate_daily_report
from strategies.engine import engine_loop  # usamos diretamente o loop, não start_engine()

async def technical_loop():
    """Loop de análise técnica periódica (placeholder)."""
    while True:
        # TODO: implementar análise técnica periódica
        await asyncio.sleep(60)

async def ml_loop():
    """Loop de análise com modelo de machine learning (placeholder)."""
    while True:
        # TODO: implementar predição periódica
        await asyncio.sleep(300)

async def agent_loop():
    """Loop de autoajuste de thresholds (placeholder)."""
    while True:
        # TODO: implementar ajuste dinâmico com base em performance
        await asyncio.sleep(600)

async def daily_report_loop():
    """Envia relatório diário via Telegram a cada 24h."""
    while True:
        now = datetime.utcnow()
        next_run = datetime(now.year, now.month, now.day) + timedelta(days=1)
        delay = (next_run - now).total_seconds()
        await asyncio.sleep(delay)
        generate_daily_report()

async def rl_loop():
    """Treina e avalia periodicamente o agente de RL."""
    agent = RLAgent(symbol=None)
    while True:
        agent.train(episodes=100)
        await asyncio.sleep(6 * 3600)
        generate_daily_report()

def start_tasks():
    """Inicia todas as tarefas assíncronas do sistema."""
    loop = asyncio.get_event_loop()
    loop.create_task(engine_loop())           # engine principal de trading
    loop.create_task(technical_loop())        # futura análise técnica
    loop.create_task(ml_loop())               # futuras predições ML
    loop.create_task(agent_loop())            # futura adaptação de thresholds
    loop.create_task(daily_report_loop())     # relatório diário
    loop.create_task(rl_loop())               # agente de RL (opcional/teste)

async def cancel_tasks():
    """Cancela todas as tasks assíncronas pendentes."""
    for t in asyncio.all_tasks():
        t.cancel()
