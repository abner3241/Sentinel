from services.telegram_service import TelegramService
from utils.config_manager import ConfigManager

async def format_and_send_alert(chat_id: int, message: str):
    """Formata e envia alerta via Telegram."""
    token = ConfigManager.get("TELEGRAM_TOKEN")
    service = TelegramService(token)
    formatted = f"⚠️ ALERT: {message}"
    await service.send_message(chat_id, formatted)
