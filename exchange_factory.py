from services.bybit_client import BybitClient
from services.binance_client import BinanceClient
from services.dry_run_client import DryRunClient

def get_exchange(name: str, **kwargs):
    name = name.lower()
    if name == 'binance':
        return BinanceClient(**kwargs)
    elif name == 'bybit':
        return BybitClient(**kwargs)
    elif name == 'dryrun':
        return DryRunClient()
    else:
        raise ValueError(f'Unknown exchange: {name}')
