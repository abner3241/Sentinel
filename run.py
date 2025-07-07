# run.py

import asyncio
from core.app import app
from core.tasks import start_tasks
from handlers.telegram import start_bot

import uvicorn


async def main():
    # Inicia tarefas em segundo plano (loops principais)
    await start_tasks()

    # Inicia bot do Telegram (escutando comandos)
    await start_bot()


if __name__ == "__main__":
    # Executa FastAPI e o restante do sistema em paralelo
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    uvicorn.run(app, host="0.0.0.0", port=8000)
