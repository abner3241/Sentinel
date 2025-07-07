import pytest
from strategies.technical import analyze_technical

@pytest.mark.asyncio
async def test_analyze_technical_empty():
    result = await analyze_technical([])
    assert isinstance(result, str)
