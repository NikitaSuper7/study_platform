import requests

from config.settings import TELEGRAM_URL, TG_BOT_TOKEN


def send_telegram_message(chat_id, message):
    """Отправляет сообщение в чат Telegram"""
    # Заполните ваш Telegram Bot API Token
    params = {
        "chat_id": chat_id,
        "text": message
    }
    requests.get(f"{TELEGRAM_URL}{TG_BOT_TOKEN}/sendMessage", params=params)