import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

class StateManager:
    _state_file = Path(__file__).resolve().parents[1] / "state.json"
    _lock = Lock()

    def __init__(self):
        self._state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        try:
            if self._state_file.exists():
                with open(self._state_file, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_state(self):
        with self._lock:
            with open(self._state_file, "w") as f:
                json.dump(self._state, f, indent=4)

    def get_order(self, signal_id: str) -> Optional[Dict[str, Any]]:
        return self._state.get("orders", {}).get(signal_id)

    def save_order(self, signal_id: str, order_data: Dict[str, Any]):
        orders = self._state.setdefault("orders", {})
        orders[signal_id] = order_data
        self._save_state()

    def remove_order(self, signal_id: str) -> bool:
        orders = self._state.get("orders", {})
        if signal_id in orders:
            orders.pop(signal_id)
            self._save_state()
            return True
        return False

    def get_risk_profile(self) -> Dict[str, Any]:
        return self._state.get("risk_profile", {})

    def set_risk_profile(self, profile: Dict[str, Any]):
        self._state["risk_profile"] = profile
        self._save_state()

    def enable_auto_indicators(self):
        self._state["auto_indicators"] = True
        self._save_state()

    def disable_auto_indicators(self):
        self._state["auto_indicators"] = False
        self._save_state()

    def is_auto_indicators_enabled(self) -> bool:
        return self._state.get("auto_indicators", False)
