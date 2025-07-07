import pytest
from types import SimpleNamespace
import asyncio

@pytest.mark.asyncio
async def test_avg_command(monkeypatch):
    # Stub avg_buy
    monkeypatch.setattr("utils.avg_buy.avg_buy", lambda: {"BTC": 45000.0})
    from handlers.telegram import avg_command
    # Dummy update and context
    class DummyMessage:
        def __init__(self):
            self.text = None
        async def reply_text(self, msg):
            self.text = msg
    dummy_update = SimpleNamespace(message=DummyMessage())
    dummy_context = SimpleNamespace(args=[])
    await avg_command(dummy_update, dummy_context)
    assert "BTC" in dummy_update.message.text
