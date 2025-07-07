import os
import asyncio
from exchange_factory import get_exchange
from utils.atr import get_latest_atr
from utils.risk_manager import check_circuit_breaker, kelly_fraction
from utils.pyramiding import calculate_pyramiding_targets
from utils.trailing_stop import trailing_stop_vwap, compute_pivots
from utils.order_flow import compute_candle_delta
from utils.hedge_strategies import hedge_market_neutral, grid_strategy
from strategies.technical import get_latest_rsi, get_latest_bollinger
from strategies.ml import predict_latest
from strategies.agent import calibrate_thresholds

RSI_THRESHOLD = float(os.getenv("RSI_THRESHOLD", 30))
PREDICTION_THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", 0.6))


async def engine_loop():
    exchange_name = os.getenv('EXCHANGE', 'dryrun')
    client = get_exchange(exchange_name)

    while True:
        try:
            symbols = await client.get_trading_symbols()

            for symbol in symbols:
                try:
                    price = await client.get_price(symbol)
                    rsi = await get_latest_rsi(symbol)
                    bollinger = await get_latest_bollinger(symbol)
                    prediction = predict_latest(symbol)
                    rsi_thresh, pred_thresh = calibrate_thresholds()

                    # Determina o lado da operação
                    side = None
                    if rsi < rsi_thresh and prediction > pred_thresh:
                        side = 'buy'
                    elif rsi > (100 - rsi_thresh) and prediction < (1 - pred_thresh):
                        side = 'sell'
                    if side is None:
                        continue

                    # Checa circuit breaker
                    if check_circuit_breaker():
                        continue

                    # Confirma via fluxo de ordens
                    delta = compute_candle_delta(symbol)
                    if (side == 'buy' and delta < 0) or (side == 'sell' and delta > 0):
                        continue

                    # Cálculo de posição via ATR
                    atr = await get_latest_atr(symbol)
                    size = kelly_fraction()

                    # Envia ordem de mercado
                    order = await client.place_order(symbol, side, size)

                    # Alvos com pyramiding
                    pyramiding_targets = calculate_pyramiding_targets(price, [0.005, 0.015, 0.03], size)
                    for tgt in pyramiding_targets:
                        await client.place_limit_order(symbol, 'sell', tgt['qty'], tgt['price'])

                    # Stop móvel baseado em VWAP
                    stop_price = trailing_stop_vwap(symbol, side, 0.005)
                    await client.modify_order_stop(order['id'], stop_price)

                    # Pivôs diários (pode ser usado em alertas visuais)
                    _ = compute_pivots(symbol)

                    # Estratégias auxiliares opcionais
                    hedge_market_neutral('BTCUSDT', 'ETHUSDT', size)
                    grid_strategy(symbol, price * 0.95, price * 1.05, levels=5, size=size)

                except Exception as e:
                    print(f"[ERRO símbolo {symbol}]: {e}")

        except Exception as e:
            print(f"[ERRO geral da engine]: {e}")

        await asyncio.sleep(60)


def start_engine():
    """Retorna a coroutine principal da engine para ser usada com loop.create_task()."""
    return engine_loop()
