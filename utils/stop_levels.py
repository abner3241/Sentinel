import os
from exchange_factory import get_exchange
from utils.atr import calculate_atr

def get_stop_levels(symbol: str,
                    api_key: str,
                    api_secret: str,
                    risk_atr_mult: float = 1.0,
                    reward_atr_mult: float = 2.0,
                    atr_period: int = 14,
                    timeframe: str = '15m') -> tuple[float, float]:
    """Calcula níveis de stop-loss e take-profit com base no ATR."""
    client = get_exchange('bybit', api_key, api_secret)
    # Fetch klines
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=atr_period+1)
    highs = [float(k['high']) for k in klines]
    lows = [float(k['low']) for k in klines]
    closes = [float(k['close']) for k in klines]
    atr = calculate_atr(highs, lows, closes, period=atr_period)
    last_price = closes[-1]
    sl = last_price - atr * risk_atr_mult
    tp = last_price + atr * reward_atr_mult
    return sl, tp
