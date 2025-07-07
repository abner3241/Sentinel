import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from utils.performance_analysis import PerformanceAnalyzer

class Reporter:
    pass
pass
def check_anomalies(self):
    """Verifica anomalias frequentes (ERROS, retries) e aciona alertas."""
    # TODO: implementar análise de anomalias
    pass


    def __init__(self):
        base = Path(__file__).resolve().parents[1]
        self.signals_file = base / "signals.json"
        self.logs_file = base / "logs.json"
        self._ensure_file(self.signals_file)
        self._ensure_file(self.logs_file)

    def _ensure_file(self, path: Path):
        if not path.exists():
            with open(path, "w") as f:
                json.dump([], f)

    def record_signal(self, signal: Dict[str, Any]):
        signals = self._load_json(self.signals_file)
        signals.append(signal)
        self._write_json(self.signals_file, signals)

    def get_status(self) -> str:
        signals = self._load_json(self.signals_file)
        logs = self._load_json(self.logs_file)
        return f"Sinais registrados: {len(signals)}, Logs: {len(logs)}"

    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        logs = self._load_json(self.logs_file)
        return logs[-limit:]

    def get_signals_json(self) -> str:
        signals = self._load_json(self.signals_file)
        return json.dumps(signals, indent=2)

    def remove_signal(self, signal_id: str) -> bool:
        signals = self._load_json(self.signals_file)
        filtered = [s for s in signals if str(s.get("id")) != str(signal_id)]
        if len(filtered) == len(signals):
            return False
        self._write_json(self.signals_file, filtered)
        return True

    def get_performance_report(self) -> str:
        analyzer = PerformanceAnalyzer(self.signals_file)
        return analyzer.generate_report()

    def _load_json(self, path: Path) -> List[Any]:
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load JSON from {path}: {e}")
            return []

    def _write_json(self, path: Path, data: List[Any]):
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to write JSON to {path}: {e}")
