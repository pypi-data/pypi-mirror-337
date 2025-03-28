from letschatty.models.chat.chat import Chat
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
class ChatHelper:

    @staticmethod
    def is_free_conversation_open(chat: Chat) -> bool:
        """
        Check if the free conversation is open.
        """
        last_incoming_message = next((msg for msg in reversed(chat.messages) if msg.is_incoming_message), None)
        if last_incoming_message is None:
            return False
        if last_incoming_message.created_at > datetime.now(tz=ZoneInfo("UTC")) - timedelta(hours=24):
            return True
        return False
