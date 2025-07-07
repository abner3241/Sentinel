import os
from exchange_factory import get_exchange

def avg_buy():
    '''Retorna um dict com avg buy de cada ativo via Bybit'''
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    client = get_exchange('bybit', api_key, api_secret)
    result = {}
    # Assumindo que client possui método get_trading_symbols()
    symbols = getattr(client, 'get_trading_symbols', lambda: [])()
    for symbol in symbols:
        # Assumindo que client possui método get_trades(symbol)
        trades = getattr(client, 'get_trades', lambda s: [])(symbol)
        buys = [t for t in trades if t.get('side', '').lower() == 'buy']
        total_qty = sum(float(t.get('qty', 0)) for t in buys)
        total_cost = sum(float(t.get('qty', 0)) * float(t.get('price', 0)) for t in buys)
        result[symbol] = round(total_cost / total_qty, 8) if total_qty else 0.0
    return result
