import os
from typing import Dict
from exchange_factory import get_exchange


def compute_vwap(symbol: str, interval: str = '1m', period: int = 60) -> float:
    """
    Calcula o VWAP (Volume Weighted Average Price) com base nos últimos `period` candles.
    """
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    klines = client.get_klines(symbol=symbol, interval=interval, limit=period)

    total_vol = 0.0
    vwap_accum = 0.0

    for k in klines:
        high = float(k['high'])
        low = float(k['low'])
        close = float(k['close'])
        vol = float(k['volume'])

        typical_price = (high + low + close) / 3
        vwap_accum += typical_price * vol
        total_vol += vol

    return vwap_accum / total_vol if total_vol > 0 else 0.0


def compute_pivots(symbol: str, interval: str = '1d') -> Dict[str, float]:
    """
    Calcula os pontos de pivô diários (Pivot Point, R1, S1) com base no penúltimo candle.
    """
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    klines = client.get_klines(symbol=symbol, interval=interval, limit=2)

    if len(klines) < 2:
        return {'pivot': 0.0, 'r1': 0.0, 's1': 0.0}

    k = klines[-2]
    high = float(k['high'])
    low = float(k['low'])
    close = float(k['close'])

    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high

    return {'pivot': pivot, 'r1': r1, 's1': s1}


def trailing_stop_vwap(symbol: str, side: str, offset_pct: float = 0.01) -> float:
    """
    Calcula um preço de stop-loss baseado na VWAP com um desvio percentual.
    - Para 'buy', stop abaixo da VWAP.
    - Para 'sell', stop acima da VWAP.
    """
    vwap = compute_vwap(symbol)

    if side.lower() == 'buy':
        return vwap * (1 - offset_pct)
    elif side.lower() == 'sell':
        return vwap * (1 + offset_pct)
    else:
        raise ValueError(f"Side inválido: {side}. Use 'buy' ou 'sell'.")
