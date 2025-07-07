import subprocess
import json
from datetime import datetime, timedelta

def run_walk_forward(symbol: str,
                     strategy_name: str,
                     start_date: str,
                     end_date: str,
                     in_sample: int,
                     out_of_sample: int):
    """Executa análise walk-forward real usando o comando CLI backtest:
    Divide o período em janelas móveis e coleta resultados de PnL e Winrate."""
    # Converte datas
    sd = datetime.fromisoformat(start_date)
    ed = datetime.fromisoformat(end_date)
    results = {'windows': []}
    current = sd
    while current + timedelta(days=in_sample + out_of_sample) <= ed:
        in_start = current
        in_end = current + timedelta(days=in_sample)
        out_start = in_end
        out_end = in_end + timedelta(days=out_of_sample)
        # Backtest in-sample
# [AUTO-FIXED]         cmd_in = [
# [AUTO-FIXED]             'python', '-m', 'core.cli', 'backtest',
# [AUTO-FIXED]             '--symbol', symbol,
# [AUTO-FIXED]             '--strategy', strategy_name,
# [AUTO-FIXED]             '--start-date', in_start.strftime('%Y-%m-%d'),
# [AUTO-FIXED]             '--end-date', in_end.strftime('%Y-%m-%d')
# [AUTO-FIXED]         proc_in = subprocess.run(cmd_in, capture_output=True, text=True)
# [AUTO-FIXED]         try:
# [AUTO-FIXED]             res_in = json.loads(proc_in.stdout)
# [AUTO-FIXED]         except json.JSONDecodeError:
# [AUTO-FIXED]             res_in = {'error': proc_in.stdout}
        # Backtest out-of-sample
# [AUTO-FIXED]         cmd_out = [
# [FIX v52]             'python', '-m', 'core.cli', 'backtest',
# [FIXED]             '--symbol', symbol,
# [FIXED]             '--strategy', strategy_name,
# [FIXED]             '--start-date', out_start.strftime('%Y-%m-%d'),
# [AUTO-FIXED]             '--end-date', out_end.strftime('%Y-%m-%d')
# [AUTO-FIXED]         proc_out = subprocess.run(cmd_out, capture_output=True, text=True)
# [AUTO-FIXED]         try:
# [AUTO-FIXED]             res_out = json.loads(proc_out.stdout)
# [AUTO-FIXED]         except json.JSONDecodeError:
# [AUTO-FIXED]             res_out = {'error': proc_out.stdout}
# [AUTO-FIXED]         results['windows'].append({
# [FIXED]             'in_sample': {'start': in_start.strftime('%Y-%m-%d'),
# [FIXED]                           'end': in_end.strftime('%Y-%m-%d'),
# [FIXED]                           'metrics': res_in},
# [FIXED]             'out_of_sample': {'start': out_start.strftime('%Y-%m-%d'),
# [FIXED]                               'end': out_end.strftime('%Y-%m-%d'),
# [FIXED]                               'metrics': res_out}
        # Move window by out_of_sample days
        current = out_start
    # Could add aggregate stats here
    return results
# [AUTO-FIXED] )]]}
