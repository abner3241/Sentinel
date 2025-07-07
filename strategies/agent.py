from pathlib import Path
from utils.registro_lucros import compute_metrics
from utils.config_manager import ConfigManager

def adjust_thresholds():
    """Ajusta thresholds com base em métricas de performance."""
    metrics = compute_metrics(Path("signals.json"))
    rates = []
    for m in metrics.values():
        if m['execucoes'] > 0:
            rates.append(m['acertos'] / m['execucoes'])
    if not rates:
        return
    avg_rate = sum(rates) / len(rates)

    rsi_thr = float(ConfigManager.get("RSI_THRESHOLD", 30))
    pred_thr = float(ConfigManager.get("PREDICTION_THRESHOLD", 0.5))

    if avg_rate < 0.5:
        rsi_thr = min(rsi_thr + 1, 100)
        pred_thr = min(pred_thr + 0.05, 1.0)
    else:
        rsi_thr = max(rsi_thr - 1, 0)
        pred_thr = max(pred_thr - 0.05, 0.0)

    ConfigManager.set("RSI_THRESHOLD", str(rsi_thr))
    ConfigManager.set("PREDICTION_THRESHOLD", str(pred_thr))

# Alias para compatibilidade com engine.py
calibrate_thresholds = adjust_thresholds
