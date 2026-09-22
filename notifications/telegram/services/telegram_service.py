import requests

from django.conf import settings


class TelegramService:

    @staticmethod
    def send_message(chat_id, message):
        url = (
            f"https://api.telegram.org/bot" f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": message,
            },
            timeout=10,
        )
        
        response.raise_for_status()
        
        return response.json()
