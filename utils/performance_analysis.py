import pandas as pd
import numpy as np
import json
from pathlib import Path

class PerformanceAnalyzer:
    def __init__(self, signals_file: Path):
        self.signals_file = signals_file

    def _load_signals(self) -> pd.DataFrame:
        try:
            df = pd.read_json(self.signals_file)
            return df
        except Exception:
            return pd.DataFrame()

    def generate_report(self) -> str:
        df = self._load_signals()
        if df.empty or "pnl" not in df.columns:
            return "Dados insuficientes para gerar relatório de performance."

        # Total PnL
        total_pnl = df["pnl"].sum()

        # Retornos diários aproximados
        returns = df["pnl"] / df.get("entry_price", 1)
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() != 0 else 0.0

        # Drawdown
        equity = returns.cumsum()
        drawdown = equity.cummax() - equity
        max_dd = drawdown.max()

        report = (
            f"Total PnL: {total_pnl:.2f}\n"
            f"Sharpe Ratio: {sharpe:.2f}\n"
            f"Max Drawdown: {max_dd:.2f}"
        )
        return report

# === Funções complementares para análise externa ===

def winrate(trades: list[dict]) -> float:
    """Calcula o winrate com base em uma lista de trades contendo 'lucro'."""
    if not trades:
        return 0.0
    ganhos = [t for t in trades if t.get("lucro", 0) > 0]
    return round(len(ganhos) / len(trades) * 100, 2)

def max_drawdown(pnl_list: list[float]) -> float:
    """Calcula o maior drawdown em uma sequência de lucros/prejuízos."""
    if not pnl_list:
        return 0.0
    max_dd = 0
    peak = pnl_list[0]
    for pnl in pnl_list:
        if pnl > peak:
            peak = pnl
        drawdown = peak - pnl
        if drawdown > max_dd:
            max_dd = drawdown
    return round(max_dd, 2)
