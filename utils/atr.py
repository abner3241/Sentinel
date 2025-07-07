# utils/atr.py

import os
from typing import List
import pandas as pd
from exchange_factory import get_exchange


def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    """
    Calcula o Average True Range (ATR) com base nas listas de preços.
    Se não houver dados suficientes, retorna uma média simples da amplitude.
    """
    if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
        trs = [highs[i] - lows[i] for i in range(1, len(highs))]
        return sum(trs) / len(trs) if trs else 0.0

    trs = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        trs.append(tr)

    return sum(trs[-period:]) / period


async def get_atr(symbol: str, period: int = 14, interval: str = '1h') -> float:
    """
    Recupera candles da exchange e calcula o ATR do símbolo especificado.
    """
    client = get_exchange(
        os.getenv('EXCHANGE', 'dryrun'),
        api_key=os.getenv('BYBIT_API_KEY'),
        api_secret=os.getenv('BYBIT_API_SECRET')
    )
    klines = await client.get_klines(symbol=symbol, interval=interval, limit=period + 1)
    highs = [float(k['high']) for k in klines]
    lows = [float(k['low']) for k in klines]
    closes = [float(k['close']) for k in klines]

    return calculate_atr(highs, lows, closes, period)


async def get_latest_atr(symbol: str, interval: str = '1h', period: int = 14) -> float:
    """
    Wrapper semântico usado pela engine para obter o ATR mais recente.
    """
    return await get_atr(symbol, period=period, interval=interval)
