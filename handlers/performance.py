from telegram import Update
from telegram.ext import ContextTypes
from utils.reporter import Reporter

async def performance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /performance."""
    report = Reporter().get_performance_report()
    await update.message.reply_text("Performance:\n" + report)
