import asyncio
from core.app import app, start_tasks, start_bot
import uvicorn

if __name__ == '__main__':
    start_tasks()
    start_bot()
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
