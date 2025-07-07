import pandas as pd
import pandas_ta as ta
from services.data_collector import DataCollector
from utils.config_manager import ConfigManager

async def analyze_technical(symbols=None) -> str:
# [AUTO-FIXED]     Calcula indicadores técnicos para os ativos especificados ou configurados.
# [AUTO-FIXED]     Retorna uma string formatada com RSI e Bandas de Bollinger para cada ativo.
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
# [AUTO-FIXED]     return "\n".join(results)
)