from typing import Optional
from exchange_factory import get_exchange
import numpy as np

def classify_regime(symbol: str,
                    api_key: str,
                    api_secret: str,
                    timeframe: str = '1d',
                    lookback: int = 30) -> str:
    """Classifica o regime de mercado ('bull', 'bear', 'sideways') com base em mudanças de preço."""
    client = get_exchange('bybit', api_key, api_secret)
    klines = client.get_klines(symbol=symbol, interval=timeframe, limit=lookback+1)
    closes = np.array([float(k['close']) for k in klines])
    returns = np.diff(closes) / closes[:-1]
    mean_ret = returns.mean()
    vol = returns.std()
    # Thresholds arbitrários: bull se mean_ret > vol, bear se mean_ret < -vol, senão sideways
    if mean_ret > vol:
        return 'bull'
    if mean_ret < -vol:
        return 'bear'
    return 'sideways'
