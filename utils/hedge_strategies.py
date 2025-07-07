import os
from exchange_factory import get_exchange

def hedge_market_neutral(symbol1: str, symbol2: str, size: float):
    """Abre posições opostas em dois símbolos correlacionados para hedge market-neutral."""
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    client = get_exchange('bybit', api_key, api_secret)
    # Buy symbol1
    order1 = client.place_order(symbol1, 'buy', size)
    # Sell symbol2 same size
    order2 = client.place_order(symbol2, 'sell', size)
    return order1, order2

def grid_strategy(symbol: str, lower_price: float, upper_price: float,
                  levels: int = 5, size: float = 1.0):
    """Cria ordens em níveis espaçados entre lower_price e upper_price para grid trading."""
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    client = get_exchange('bybit', api_key, api_secret)
    step = (upper_price - lower_price) / (levels - 1)
    orders = []
    for i in range(levels):
        price = lower_price + step * i
        orders.append(client.place_limit_order(symbol, 'buy', size, price))
    return orders
