import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, List, Optional

def load_signals(signals_file: Path) -> List[Dict[str, Any]]:
    """Carrega sinais de um arquivo JSON."""
    try:
        with open(signals_file, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def compute_metrics(signals_file: Path) -> Dict[str, Dict[str, Any]]:
# [AUTO-FIXED]     Computa métricas por estratégia e ativo:
# [AUTO-FIXED]     - acertos: contagem de sinais com pnl > 0
# [AUTO-FIXED]     - erros: contagem de sinais com pnl <= 0
# [AUTO-FIXED]     - lucro_total: soma de pnl positivo
# [AUTO-FIXED]     - execucoes: total de sinais
# [AUTO-FIXED]     - ult_execucao: timestamp ISO da última execução
    signals = load_signals(signals_file)
    metrics: Dict[str, Dict[str, Any]] = {}
    for s in signals:
        strat = s.get('strategy', 'default')
        asset = s.get('symbol', s.get('symbol', 'unknown'))
        key = f"{strat}/{asset}"
# [AUTO-FIXED]         m = metrics.setdefault(key, {
# [AUTO-FIXED]             'acertos': 0,
# [AUTO-FIXED]             'erros': 0,
# [AUTO-FIXED]             'lucro_total': 0.0,
# [AUTO-FIXED]             'execucoes': 0,
# [AUTO-FIXED]             'ult_execucao': None
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
# [AUTO-FIXED]     Retorna o PnL total do dia especificado (ou de hoje, por padrão).
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
# [AUTO-FIXED] )}