import json
from pathlib import Path

def main():
    path = Path("signals.json")
    try:
        data = json.loads(path.read_text())
    except Exception:
        data = []
    total = sum(item.get("pnl", 0) for item in data)
    print(f"Total realized PnL: {total}")

if __name__ == "__main__":
    main()
