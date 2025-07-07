from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import asyncio

import core.tasks as tasks
from dashboard.api import router as dashboard_router
from handlers.telegram import start_bot

app = FastAPI()

# Mount dashboard UI
app.mount("/ui", StaticFiles(directory="dashboard/ui", html=True), name="ui")
app.include_router(dashboard_router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    tasks.start_tasks()
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())


@app.on_event("shutdown")
async def on_shutdown():
    pass
