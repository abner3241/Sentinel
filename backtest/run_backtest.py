import argparse
import asyncio
import pandas as pd
from services.data_collector import DataCollector
from strategies.engine import generate_signals

def main():
    parser = argparse.ArgumentParser(description="Backtest CriptoSentinel strategies")
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="Symbol to backtest")
    parser.add_argument("--interval", type=str, default="1h", help="Candlestick interval")
    parser.add_argument("--limit", type=int, default=1000, help="Number of bars")
    args = parser.parse_args()

    dc = DataCollector()
    data = asyncio.run(dc.get_historical(args.symbol, interval=args.interval, limit=args.limit))
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} bars for {args.symbol}")
    # Simulate signal generation
    signals = asyncio.run(generate_signals())
    print(f"Generated {len(signals)} signals")
