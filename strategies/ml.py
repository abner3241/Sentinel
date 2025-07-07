import asyncio
from services.data_collector import DataCollector
from utils.config_manager import ConfigManager
import os
import pandas as pd
import joblib
from services.data_collector import DataCollector
from utils.config_manager import ConfigManager
from sklearn.ensemble import RandomForestClassifier

async def run_ml_pipeline():
# [AUTO-FIXED]     Executa pipeline de ML para cada ativo configurado:
# [AUTO-FIXED]     - Coleta dados históricos
# [AUTO-FIXED]     - Extrai features simples (retorno)
# [AUTO-FIXED]     - Treina ou carrega modelo
# [AUTO-FIXED]     - Gera predições salvas no arquivo de modelo
    assets = ConfigManager.get_list("ASSETS")
    dc = DataCollector()
    window = ConfigManager.get_int("ML_WINDOW", 500)
    for symbol in assets:
        raw = await dc.get_historical(symbol, interval="1h", limit=window)
        df = pd.DataFrame(raw)
        df.columns = [c.lower() for c in df.columns]
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        # Feature: retorno percentual
        df['return'] = df['close'].pct_change()
        df.dropna(inplace=True)
        X = df[['return']]
        y = (df['return'].shift(-1) > 0).astype(int)
        model_path = ConfigManager.get("ML_MODEL_PATH", f"models/{symbol}_model.pkl")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            model = RandomForestClassifier(n_estimators=100)
            model.fit(X, y)
            joblib.dump(model, model_path)
        # Adiciona predição ao DataFrame (exemplo)
        df['prediction'] = model.predict(X)
    # Retorna sem sinal direto


def predict_latest(symbol: str) -> float:
    """Retorna probabilidade da classe 1 (preço subir) do último bar."""
    import joblib
    from pathlib import Path
    model_path = ConfigManager.get("ML_MODEL_PATH", f"models/{symbol}_model.pkl")
    if not Path(model_path).exists():
        return 0.0
    model = joblib.load(model_path)
    # obter último return
    dc = DataCollector()
    raw = asyncio.run(dc.get_historical(symbol, interval="1h", limit=2))
    import pandas as pd
    df = pd.DataFrame(raw)
    df.columns = [c.lower() for c in df.columns]
    df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)
    df['return'] = df['close'].pct_change()
    latest_ret = df['return'].dropna().iloc[-1]
    prob = model.predict_proba([[latest_ret]])[0][1]
    return prob
