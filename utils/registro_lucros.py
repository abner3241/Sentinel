import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import pandas as pd

HISTORICO_PATH = Path("historico_sinais.json")  # caminho padrão usado por outras funções

def load_signals(signals_file: Path) -> List[Dict[str, Any]]:
    """Carrega sinais de um arquivo JSON."""
    try:
        with open(signals_file, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def compute_metrics(signals_file: Path) -> Dict[str, Dict[str, Any]]:
    """Computa métricas por estratégia e ativo."""
    signals = load_signals(signals_file)
    metrics: Dict[str, Dict[str, Any]] = {}

    for s in signals:
        strat = s.get('strategy', 'default')
        asset = s.get('symbol', 'unknown')
        key = f"{strat}/{asset}"

        m = metrics.setdefault(key, {
            'acertos': 0,
            'erros': 0,
            'lucro_total': 0.0,
            'execucoes': 0,
            'ult_execucao': None
        })

        pnl = s.get('pnl', 0.0)
        if pnl > 0:
            m['acertos'] += 1
            m['lucro_total'] += pnl
        else:
            m['erros'] += 1

        m['execucoes'] += 1

        ts = s.get('timestamp')
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                if not m['ult_execucao'] or dt > datetime.fromisoformat(m['ult_execucao']):
                    m['ult_execucao'] = dt.isoformat()
            except ValueError:
                pass

    return metrics

def get_daily_pnl(signals_file: Path, target_date: Optional[date] = None) -> float:
    """Retorna o PnL total do dia especificado (ou de hoje, por padrão)."""
    signals = load_signals(signals_file)
    total = 0.0
    date_obj = target_date or date.today()

    for s in signals:
        ts = s.get('timestamp')
        pnl = s.get('pnl', 0.0)
        if ts:
            try:
                dt = datetime.fromisoformat(ts).date()
                if dt == date_obj:
                    total += pnl
            except ValueError:
                pass

    return total

def get_historic_pnl(days: int = 30) -> pd.DataFrame:
    """Retorna o DataFrame de PnL diário dos últimos X dias."""
    try:
        df = pd.read_json(HISTORICO_PATH)
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values('data', ascending=False).head(days)
        return df[['data', 'pnl']]
    except Exception as e:
        print(f"[ERRO] Falha ao carregar histórico de lucros: {e}")
        return pd.DataFrame(columns=['data', 'pnl'])
