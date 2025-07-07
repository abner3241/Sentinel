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
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() != 0 else np.nan
        # Drawdown
        equity = returns.cumsum()
        drawdown = equity.cummax() - equity
        max_drawdown = drawdown.max()
        report = (
            f"Total PnL: {total_pnl:.2f}\n"
            f"Sharpe Ratio: {sharpe:.2f}\n"
            f"Max Drawdown: {max_drawdown:.2f}"
# [AUTO-FIXED]         return report
)