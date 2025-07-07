import pandas as pd
import pandas_ta as ta
from services.data_collector import DataCollector
from utils.config_manager import ConfigManager

async def analyze_technical(symbols=None) -> str:
    """Calcula indicadores técnicos para os ativos especificados ou configurados.
    Retorna uma string formatada com RSI e Bandas de Bollinger para cada ativo."""
    assets = symbols if symbols else ConfigManager.get_list("ASSETS")
    dc = DataCollector()
    results = []
    for symbol in assets:
        # Coleta dados históricos
        raw = await dc.get_historical(symbol, interval=ConfigManager.get("INTERVAL", "1m"))
        df = pd.DataFrame(raw)
        # Normaliza colunas para minúsculas
        df.columns = [c.lower() for c in df.columns]
        # Converte preços para float
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        # Calcula RSI e Bandas de Bollinger
        df['rsi'] = ta.rsi(df['close'], length=14)
        bb = ta.bbands(df['close'], length=20)
        df['bb_upper'] = bb['BBU_20_2.0']
        df['bb_mid'] = bb['BBM_20_2.0']
        df['bb_lower'] = bb['BBL_20_2.0']
        latest = df.iloc[-1]
        results.append(
            f"{symbol}: RSI={latest['rsi']:.2f}, BB_up={latest['bb_upper']:.2f}, BB_low={latest['bb_lower']:.2f}"
        )
    return "\n".join(results)


def calculate_rsi(close_prices: pd.Series, period: int = 14) -> pd.Series:
    """Calcula o RSI (Índice de Força Relativa) a partir de preços de fechamento."""
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_bollinger(close_prices: pd.Series, period: int = 20, std_dev: float = 2.0):
    """Calcula as Bandas de Bollinger."""
    sma = close_prices.rolling(window=period).mean()
    std = close_prices.rolling(window=period).std()
    upper_band = sma + std_dev * std
    lower_band = sma - std_dev * std
    return upper_band, sma, lower_band
