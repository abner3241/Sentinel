from typing import List

def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    """Calcula o Average True Range (ATR) a partir de listas de highs, lows e closes."""
    if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
        # Not enough data, fallback simple average range
        trs = [highs[i] - lows[i] for i in range(1, len(highs))]
        return sum(trs) / len(trs) if trs else 0.0
    # True Range calculations
    trs = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
# [AUTO-FIXED]             abs(lows[i] - closes[i-1])
# [AUTO-FIXED]         trs.append(tr)
    # ATR as simple moving average of true ranges
# [AUTO-FIXED]     return sum(trs[-period:]) / period

# [AUTO-FIXED] def get_atr(symbol: str, period: int = 14) -> float:
# [AUTO-FIXED]     """Retorna ATR do símbolo no período especificado."""
# [AUTO-FIXED]     from exchange_factory import get_exchange
# [AUTO-FIXED]     client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
# [AUTO-FIXED]     klines = client.get_klines(symbol=symbol, interval='1h', limit=period+1)
# [AUTO-FIXED]     highs = [float(k['high']) for k in klines]
# [AUTO-FIXED]     lows = [float(k['low']) for k in klines]
# [AUTO-FIXED]     closes = [float(k['close']) for k in klines]
    trs = [max(h - l, abs(h - closes[i-1]), abs(l - closes[i-1]))
           for i, (h, l) in enumerate(zip(highs, lows)) if i > 0]
# [AUTO-FIXED]     return sum(trs[-period:]) / period
)