import os
import json
from threading import Lock
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

class ConfigManager:
    _config_file = Path(__file__).resolve().parents[1] / "config.json"
    _config: Dict[str, Any] = {}
    _lock = Lock()
    # Load existing config from file if present
    try:
        if _config_file.exists():
            with open(_config_file, "r") as f:
                _config = json.load(f)
    except Exception:
        _config = {}

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        # Check environment variables first
        value = os.getenv(key)
        if value is not None:
            return value
        # Then check config file
        return cls._config.get(key, default)

    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        value = cls.get(key)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def get_list(cls, key: str, delimiter: str = ",") -> List[str]:
        value = cls.get(key, "")
        if not value:
            return []
        return [item.strip() for item in value.split(delimiter) if item.strip()]

    @classmethod
    def set(cls, key: str, value: Union[str, int, List[str]]) -> None:
        with cls._lock:
            # Store as string or list
            if isinstance(value, list):
                cls._config[key] = value
            else:
                cls._config[key] = str(value)
            # Write back to config file
            try:
                with open(cls._config_file, "w") as f:
                    json.dump(cls._config, f, indent=4)
            except Exception as e:
                raise RuntimeError(f"Failed to write config file: {e}")

    @classmethod
    def list_all(cls) -> Dict[str, Optional[str]]:
        # Merge environment and config file
        merged: Dict[str, Optional[str]] = {}
        # Environment vars
        for key, value in os.environ.items():
            merged[key] = value
        # Config file overrides or adds
        for key, value in cls._config.items():
            merged[key] = value
        return merged
