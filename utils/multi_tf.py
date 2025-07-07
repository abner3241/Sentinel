from exchange_factory import get_exchange
import numpy as np

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    ups = deltas[deltas > 0]
    downs = -deltas[deltas < 0]
    avg_up = ups.mean() if ups.size else 0.0
    avg_down = downs.mean() if downs.size else 0.0
    rs = avg_up / avg_down if avg_down else 0.0
    return 100 - 100 / (1 + rs)

def confirm_multi_tf(symbol: str,
                    api_key: str,
                    api_secret: str,
                    tf_short: str = '15m',
                    tf_long: str = '1h',
                    rsi_period: int = 14,
                    lower_thresh: float = 30.0,
                    upper_thresh: float = 70.0) -> str | None:
    """Confirma sinal se RSI em ambos timeframes concorda: 'buy', 'sell' ou None"""
    client = get_exchange('bybit', api_key, api_secret)
    # Short timeframe
    klines_s = client.get_klines(symbol=symbol, interval=tf_short, limit=rsi_period + 1)
    closes_s = [float(k['close']) for k in klines_s]
    rsi_s = calculate_rsi(closes_s, period=rsi_period)
    # Long timeframe
    klines_l = client.get_klines(symbol=symbol, interval=tf_long, limit=rsi_period + 1)
    closes_l = [float(k['close']) for k in klines_l]
    rsi_l = calculate_rsi(closes_l, period=rsi_period)
    # Confirm
    if rsi_s < lower_thresh and rsi_l < lower_thresh:
        return 'buy'
    if rsi_s > upper_thresh and rsi_l > upper_thresh:
        return 'sell'
    return None
