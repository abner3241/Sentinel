import pytest
from handlers.telegram import start_command
from telegram import Update, Message
from telegram.ext import ContextTypes

class DummyMessage:
    def __init__(self):
        self.text = ""
        self.replies = []
    async def reply_text(self, text):
        self.replies.append(text)

class DummyUpdate:
    def __init__(self):
        self.message = DummyMessage()

@pytest.mark.asyncio
async def test_start_command():
    update = DummyUpdate()
    context = ContextTypes.DEFAULT_TYPE()
    await start_command(update, context)
    assert "Bem-vindo" in update.message.replies[0]
