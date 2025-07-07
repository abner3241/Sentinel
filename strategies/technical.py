import pandas as pd
import pandas_ta as ta
from services.data_collector import DataCollector
from utils.config_manager import ConfigManager


async def analyze_technical(symbols=None) -> str:
    """
    Calcula indicadores técnicos (RSI e Bandas de Bollinger)
    para os ativos especificados ou configurados.
    Retorna uma string formatada para exibição.
    """
    assets = symbols if symbols else ConfigManager.get_list("ASSETS")
    dc = DataCollector()
    results = []
    for symbol in assets:
        # Coleta dados históricos
        raw = await dc.get_historical(symbol, interval=ConfigManager.get("INTERVAL", "1m"))
        df = pd.DataFrame(raw)

        # Normaliza colunas e converte tipos
        df.columns = [c.lower() for c in df.columns]
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
    """
    Calcula o RSI (Índice de Força Relativa) a partir de uma série de preços.
    """
    delta = close_prices.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss.replace(0, 1e-10)  # evita divisão por zero
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger(close_prices: pd.Series, period: int = 20, std_dev: float = 2.0):
    """
    Calcula as Bandas de Bollinger para uma série de preços.
    """
    sma = close_prices.rolling(window=period).mean()
    std = close_prices.rolling(window=period).std()
    upper_band = sma + std_dev * std
    lower_band = sma - std_dev * std
    return upper_band, sma, lower_band


async def get_latest_rsi(symbol: str, period: int = 14) -> float:
    """
    Retorna o valor mais recente do RSI do símbolo.
    """
    dc = DataCollector()
    raw = await dc.get_historical(symbol, interval=ConfigManager.get("INTERVAL", "1m"))
    df = pd.DataFrame(raw)
    df.columns = [c.lower() for c in df.columns]
    df['close'] = df['close'].astype(float)
    rsi_series = calculate_rsi(df['close'], period)
    return float(rsi_series.dropna().iloc[-1])


async def get_latest_bollinger(symbol: str, period: int = 20, std_dev: float = 2.0):
    """
    Retorna as bandas de Bollinger mais recentes para um símbolo.
    """
    dc = DataCollector()
    raw = await dc.get_historical(symbol, interval=ConfigManager.get("INTERVAL", "1m"))
    df = pd.DataFrame(raw)
    df.columns = [c.lower() for c in df.columns]
    df['close'] = df['close'].astype(float)
    upper, mid, lower = calculate_bollinger(df['close'], period, std_dev)
    return float(upper.dropna().iloc[-1]), float(mid.dropna().iloc[-1]), float(lower.dropna().iloc[-1])
