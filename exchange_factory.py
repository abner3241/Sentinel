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
        return EnhancedDryRunClient()
    else:
        raise ValueError(f'Unknown exchange: {name}')

# Extensão do cliente dryrun para testes locais
class EnhancedDryRunClient(DryRunClient):
    def get_trading_symbols(self):
        # Simula dois ativos padrão
        return ["BTCUSDT", "ETHUSDT"]
