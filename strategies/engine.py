import os
import asyncio
from exchange_factory import get_exchange
from utils.atr import get_atr
from utils.risk_manager import check_circuit_breaker, kelly_fraction
from utils.pyramiding import calculate_pyramiding_targets
from utils.trailing_stop import trailing_stop_vwap, compute_pivots
from utils.order_flow import compute_candle_delta
from utils.hedge_strategies import hedge_market_neutral, grid_strategy
from strategies.technical import calculate_rsi, calculate_bollinger
from strategies.ml import predict_latest
from strategies.agent import calibrate_thresholds

RSI_THRESHOLD = float(os.getenv("RSI_THRESHOLD", 30))
PREDICTION_THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", 0.6))

async def engine_loop():
    exchange_name = os.getenv('EXCHANGE', 'dryrun')
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    client = get_exchange(exchange_name, api_key, api_secret)

    while True:
        symbols = client.get_trading_symbols()
        for symbol in symbols:
            price = client.get_price(symbol)
            rsi = calculate_rsi(symbol)
            bollinger = calculate_bollinger(symbol)
            prediction = predict_latest(symbol)
            rsi_thresh, pred_thresh = calibrate_thresholds()

            # Determine side
            side = None
            if rsi < rsi_thresh and prediction > pred_thresh:
                side = 'buy'
            elif rsi > 100 - rsi_thresh and prediction < 1 - pred_thresh:
                side = 'sell'
            if side is None:
                continue

            # Circuit breaker
            if check_circuit_breaker():
                continue

            # Candle delta confirmation
            delta = compute_candle_delta(symbol)
            if (side == 'buy' and delta < 0) or (side == 'sell' and delta > 0):
                continue

            # Position sizing
            atr = get_atr(symbol)
            size = kelly_fraction()

            # Place market order
            order = client.place_order(symbol, side, size)

            # Pyramiding exits
            pyramiding_targets = calculate_pyramiding_targets(price, [0.005, 0.015, 0.03], size)
            for tgt in pyramiding_targets:
                client.place_limit_order(symbol, 'sell', tgt['qty'], tgt['price'])

            # Apply trailing stop
            stop_price = trailing_stop_vwap(symbol, side, 0.005)
            client.modify_order_stop(order['id'], stop_price)

            # Compute daily pivots
            pivots = compute_pivots(symbol)

            # Optional hedge and grid examples
            hedge_market_neutral('BTCUSDT', 'ETHUSDT', size)
            grid_strategy(symbol, price * 0.95, price * 1.05, levels=5, size=size)

        await asyncio.sleep(60)

def start_engine():
    """Retorna a coroutine principal da engine para ser usada com loop.create_task()."""
    return engine_loop()
