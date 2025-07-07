import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_ts_model(symbol: str,
                   api_key: str,
                   api_secret: str,
                   model_type: str = 'rf',
                   epochs: int = 10,
                   model_path: str = None):
    from exchange_factory import get_exchange
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    klines = client.get_klines(symbol=symbol, interval='1h', limit=500)
    df = pd.DataFrame(klines)
    df['close'] = df['close'].astype(float)
    for lag in range(1, 6):
        df[f'ret_lag_{lag}'] = df['close'].pct_change(lag)
    df.dropna(inplace=True)
    X = df[[f'ret_lag_{lag}' for lag in range(1, 6)]].values[:-1]
    y = df['close'].pct_change().shift(-1).dropna().values
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    if not model_path:
        model_path = f"models/ts/{symbol}_{model_type}.pkl"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    return model_path

def predict_ts(symbol: str,
               api_key: str,
               api_secret: str,
               model_type: str = 'rf',
               model_path: str = None):
    if model_path and os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        raise ValueError("Modelo não encontrado")
    from exchange_factory import get_exchange
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    klines = client.get_klines(symbol=symbol, interval='1h', limit=6)
    df = pd.DataFrame(klines)
    df['close'] = df['close'].astype(float)
    features = np.array([df['close'].pct_change(lag).iloc[-lag] for lag in range(1,6)])
    pred = model.predict(features.reshape(1, -1))[0]
    return pred
