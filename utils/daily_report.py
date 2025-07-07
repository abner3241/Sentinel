import os
from datetime import datetime
from telegram import Bot
from utils.registro_lucros import get_daily_pnl
from utils.performance_analysis import winrate, max_drawdown
from utils.metrics import ORDER_COUNTER, ORDER_LATENCY, PNL_GAUGE

def generate_daily_report() -> str:
    """Gera relatório de PnL, winrate, drawdown e R-multiplier para o dia atual."""
    # Daily PnL
    pnl = get_daily_pnl()
    # Winrate e drawdown - assume functions take a date or default to today
    wr = winrate()
    dd = max_drawdown()
    # R-multiplier = (mean gain / mean loss)
    avg_gain = PNL_GAUGE.labels(result='gain')._value.get() if hasattr(PNL_GAUGE, 'labels') else 0
    avg_loss = abs(PNL_GAUGE.labels(result='loss')._value.get()) if hasattr(PNL_GAUGE, 'labels') else 0
    r_mult = (avg_gain/avg_loss) if avg_loss else float('inf')
    report = [
        f"📊 Relatório Diário - {datetime.utcnow().strftime('%Y-%m-%d')}",
        f"PnL Diário: {pnl:.2f} USDT",
        f"Winrate: {wr*100:.2f}%",
        f"Max Drawdown: {dd*100:.2f}%",
        f"R-multiplier: {r_mult:.2f}",
# [AUTO-FIXED]     return "\n".join(report)

# [AUTO-FIXED] def send_daily_report():
# [AUTO-FIXED]     """Envia o relatório diário via Telegram"""
# [AUTO-FIXED]     token = os.getenv('TELEGRAM_BOT_TOKEN')
# [AUTO-FIXED]     chat_id = os.getenv('TELEGRAM_CHAT_ID')
# [AUTO-FIXED]     if not token or not chat_id:
# [AUTO-FIXED]         return
# [AUTO-FIXED]     bot = Bot(token=token)
# [AUTO-FIXED]     report = generate_daily_report()
    bot.send_message(chat_id=chat_id, text=report)
]