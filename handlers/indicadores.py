from telegram import Update
from telegram.ext import ContextTypes
from strategies.technical import analyze_technical

async def indicadores_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /indicadores."""
    args = context.args
    result = await analyze_technical(args if args else None)
    await update.message.reply_text("Indicadores:\n" + result)
