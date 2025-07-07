import time
from typing import Optional
from exchange_factory import get_exchange

def twap_order(symbol: str,
               side: str,
               total_size: float,
               api_key: str,
               api_secret: str,
               slices: int = 5,
               interval_sec: int = 60) -> None:
    """Executa ordens TWAP (Time-Weighted Average Price)."""
    client = get_exchange('bybit', api_key, api_secret)
    size_per_slice = total_size / slices if slices > 0 else total_size
    for i in range(slices):
        client.place_order(symbol, side, size_per_slice)
        time.sleep(interval_sec)

def simulate_slippage(size: float,
                      slippage_pct: float = 0.001) -> float:
    """Calcula tamanho ajustado pelo slippage estimado."""
    return size * (1 - slippage_pct)
