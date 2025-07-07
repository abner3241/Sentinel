import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils.pyramiding import calculate_pyramiding_targets
from utils.trailing_stop import compute_vwap, trailing_stop_vwap, compute_pivots
from utils.order_flow import compute_candle_delta
from utils.hedge_strategies import hedge_market_neutral, grid_strategy

print(f"🔑 TOKEN DETECTADO: {os.getenv('TELEGRAM_BOT_TOKEN')}")

app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
bot = app.bot

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CriptoSentinel iniciado!")

async def pyramiding_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Uso: /pyramiding ENTRY_PRICE [SIZE]")
        return
    entry = float(args[0])
    size = float(args[1]) if len(args) > 1 else 1.0
    targets = calculate_pyramiding_targets(entry, [0.005,0.015,0.03], size)
    msg = "\n".join(f"Sell {t['qty']} @ {t['price']}" for t in targets)
    await update.message.reply_text(msg)

async def trailing_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Uso: /trailing_stop SYMBOL buy|sell [offset]")
        return
    symbol, side = args[0], args[1]
    offset = float(args[2]) if len(args) > 2 else 0.005
    vwap = compute_vwap(symbol)
    stop = trailing_stop_vwap(symbol, side, offset)
    piv = compute_pivots(symbol)
    msg = f"VWAP: {vwap:.4f}\nStop: {stop:.4f}\nPivot={piv['pivot']:.4f}, R1={piv['r1']:.4f}, S1={piv['s1']:.4f}"
    await update.message.reply_text(msg)

async def candle_delta_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Uso: /candle_delta SYMBOL [limit]")
        return
    symbol = args[0]
    limit = int(args[1]) if len(args) > 1 else 200
    delta = compute_candle_delta(symbol, limit)
    await update.message.reply_text(f"Candle Delta: {delta}")

async def hedge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Uso: /hedge SYMBOL1 SYMBOL2 SIZE")
        return
    s1, s2, size = args[0], args[1], float(args[2])
    o1, o2 = hedge_market_neutral(s1, s2, size)
    await update.message.reply_text(f"Hedged: {o1}, {o2}")

async def grid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Uso: /grid SYMBOL LOWER UPPER [LEVELS] [SIZE]")
        return
    symbol = args[0]
    lower, upper = float(args[1]), float(args[2])
    levels = int(args[3]) if len(args) > 3 else 5
    size = float(args[4]) if len(args) > 4 else 1.0
    orders = grid_strategy(symbol, lower, upper, levels=levels, size=size)
    msg = "\n".join(str(o) for o in orders)
    await update.message.reply_text(msg)

# Register handlers
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("pyramiding", pyramiding_command))
app.add_handler(CommandHandler("trailing_stop", trailing_stop_command))
app.add_handler(CommandHandler("candle_delta", candle_delta_command))
app.add_handler(CommandHandler("hedge", hedge_command))
app.add_handler(CommandHandler("grid", grid_command))

async def start_bot():
    await asyncio.to_thread(app.run_polling)
