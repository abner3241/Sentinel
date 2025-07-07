from typing import List
import os
from exchange_factory import get_exchange

def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    """Calcula o Average True Range (ATR) a partir de listas de highs, lows e closes."""
    if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
        # Dados insuficientes, fallback para média simples da amplitude
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

def get_atr(symbol: str, period: int = 14) -> float:
    """Retorna o ATR do símbolo consultando a exchange."""
    client = get_exchange(
        'bybit',
        os.getenv('BYBIT_API_KEY'),
        os.getenv('BYBIT_API_SECRET')
    )
    klines = client.get_klines(symbol=symbol, interval='1h', limit=period + 1)
    highs = [float(k['high']) for k in klines]
    lows = [float(k['low']) for k in klines]
    closes = [float(k['close']) for k in klines]

    return calculate_atr(highs, lows, closes, period)
