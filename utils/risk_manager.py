import os
from datetime import datetime, timedelta
from utils.registro_lucros import get_daily_pnl, get_historic_pnl
from utils.performance_analysis import max_drawdown

def position_size_by_atr(capital: float, atr: float, risk_pct: float) -> float:
    """Calcula tamanho da posição para que o risco (stop*atr) não exceda risk_pct do capital."""
    if atr <= 0:
        return 0.0
    return (capital * risk_pct) / atr

def kelly_fraction(win_rate: float, win_loss_ratio: float) -> float:
    """Calcula fração de Kelly: f* = W - (1 - W)/R"""
    return max(0.0, win_rate - (1 - win_rate) / win_loss_ratio)

def check_circuit_breaker(threshold_pct: float = 0.1) -> bool:
    """Verifica se o drawdown dos últimos 24h excede threshold_pct."""
    end = datetime.utcnow()
    start = end - timedelta(hours=24)
    # usa histórico de PnL; get_historic_pnl retorna lista de {'timestamp':..., 'pnl':...}
    hist = get_historic_pnl(start, end)
    pnl_series = [item['pnl'] for item in hist]
    dd = max_drawdown(pnl_series)
    return dd > threshold_pct
