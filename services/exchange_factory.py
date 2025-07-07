
from utils.config_manager import ConfigManager
from services.binance_client import BinanceClient
from services.bybit_client import BybitClient
from services.dryrun_client import DryRunClient

class ExchangeFactory:
    @staticmethod
    def get_client():
        exchange = ConfigManager.get("EXCHANGE", "binance").lower()
        api_key = ConfigManager.get("API_KEY")
        api_secret = ConfigManager.get("API_SECRET")
        testnet = ConfigManager.get("TESTNET", "true").lower() == "true"

        if exchange == "binance":
            return BinanceClient(api_key=api_key, api_secret=api_secret, testnet=testnet)
        elif exchange == "bybit":
            return BybitClient(api_key=api_key, api_secret=api_secret, testnet=testnet)
        else:
            return DryRunClient()
