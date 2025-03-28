from letschatty.models.chat.continuous_conversation import ContinuousConversation, ContinuousConversationStatus
from letschatty.models.utils.types.message_types import MessageType
from letschatty.models.messages.chatty_messages.base.message_draft import SendMessagesFromAgentToChat, MessageDraft
from letschatty.models.chat.chat import Chat
from letschatty.models.messages.chatty_messages import ChattyMessage
from letschatty.models.messages.chatty_messages.button import ButtonMessage
from typing import Optional, List
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData, FilledRecipientParameter, TemplateOrigin
from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate
from letschatty.services.factories.messages.central_notification_factory import CentralNotificationFactory
from letschatty.models.messages.chatty_messages.schema.chatty_content.content_central import ChattyContentCentral, CentralNotificationStatus
from letschatty.models.chat.scheduled_messages import ScheduledMessages
from letschatty.models.utils.custom_exceptions import NotFoundError
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
logger = logging.getLogger(__name__)


class ContinuousConversationHelper:

    @staticmethod
    def build_filled_template_data(chat: Chat, cc: ContinuousConversation, template_name: str) -> FilledTemplateData:
        """
        Build the filled template data for a continuous conversation.
        """
        preview_message = ContinuousConversationHelper.get_preview_message(cc=cc)
        filled_recipient_parameters = [FilledRecipientParameter(id="preview_message", text=preview_message)]
        filled_template_data = FilledTemplateData(
            template_name=template_name,
            area=chat.area,
            agent_email=cc.agent_email,
            phone_number=chat.client.waid,
            parameters=filled_recipient_parameters,
            description="Continuous conversation request",
            forced_send=True,
            origin=TemplateOrigin.FROM_CONTINUOUS_CONVERSATION
            )
        return filled_template_data

    @staticmethod
    def get_preview_message(cc: ContinuousConversation) -> Optional[str]:
        """
        Get the preview message for a continuous conversation.
        The preview is the first message of the continuous conversation (or a part of it if its too long, and it'll only be text for now)
        """
        preview_message = cc.messages[0]
        preview = preview_message.content.get_body_or_caption()
        if len(preview) > 150:
            return preview[:150] + "..."
        else:
            return preview

    @staticmethod
    def create_continuous_conversation(chat: Chat, messages:SendMessagesFromAgentToChat) -> ContinuousConversation:
        """
        Create a new continuous conversation from a list of messages.
        """
        active_cc = ContinuousConversationHelper.get_active_cc(chat)
        if active_cc:
            raise ValueError("There is already an active continuous conversation")
        cc = ContinuousConversation(messages=messages.messages, agent_email=messages.agent_email, forced_send=messages.forced_send)
        chat.continuous_conversations.append(cc)
        return cc

    @staticmethod
    def update_continuous_conversation(chat: Chat, cc_id: str, messages: SendMessagesFromAgentToChat) -> ContinuousConversation:
        """
        Update a continuous conversation from a list of messages.
        """
        cc = ContinuousConversationHelper.get_cc_by_id(chat=chat, cc_id=cc_id)
        if not cc.active:
            raise ValueError("Cannot update a non-active continuous conversation")
        new_cc = ContinuousConversation(messages=messages.messages, agent_email=messages.agent_email, forced_send=messages.forced_send)
        cc.messages = new_cc.messages
        cc.forced_send = new_cc.forced_send
        cc.expires_at = new_cc.expires_at
        cc.updated_at = datetime.now(ZoneInfo("UTC"))
        cc.agent_email = new_cc.agent_email
        return cc

    @staticmethod
    def get_active_cc(chat: Chat) -> Optional[ContinuousConversation]:
        """
        Check if a continuous conversation is active.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.active), None)
        if cc and cc.is_expired and not cc.forced_send:
            cc.set_status(status=ContinuousConversationStatus.EXPIRED)
            body = f"Continuous conversation expired at {cc.expires_at}"
            central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
            central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
            chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def get_cc_by_message_id(chat: Chat, message_id: str) -> Optional[ContinuousConversation]:
        """
        Get a continuous conversation by message id.
        """
        return next((cc for cc in chat.continuous_conversations if cc.template_message_waid == message_id), None)

    @staticmethod
    def get_cc_by_id(chat: Chat, cc_id: str) ->ContinuousConversation:
        """
        Get a continuous conversation by id.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.id == cc_id), None)
        if cc and cc.forced_send:
            raise NotFoundError(f"Continuous conversation with id {cc_id} not found")
        return cc

    @staticmethod
    def cancel_continuous_conversation(chat: Chat, cc_id: str) -> Optional[ContinuousConversation]:
        """
        Cancel a continuous conversation.

        Args:
            chat: The chat containing the CC
            cc_id: The ID of the CC to cancel

        Returns:
            The canceled continuous conversation, or None if not found
        """
        cc = ContinuousConversationHelper.get_cc_by_id(chat=chat, cc_id=cc_id)
        if cc:
            cc.set_status(status=ContinuousConversationStatus.CANCELLED)
            body = f"Continuous conversation cancelled by the agent {chat.agent_id}"
            logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
            central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.ERROR, calls_to_action=cc.calls_to_action)
            central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
            chat.add_central_notification(central_notif)
        else:
            raise NotFoundError(f"Continuous conversation with id {cc_id} not found")
        return cc

    @staticmethod
    def dump_active_cc(chat: Chat) -> Chat:
        """
        Dump the active continuous conversation.
        """
        cc = ContinuousConversationHelper.get_active_cc(chat)
        if not cc:
            return chat
        chat.messages.extend(cc.messages)
        return chat

    @staticmethod
    def get_cc_messages(chat: Chat, cc_id: str  ) -> List[MessageDraft]:
        """
        Get the messages of the active continuous conversation.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.id == cc_id), None)
        if not cc:
            raise ValueError(f"Continuous conversation with id {cc_id} not found")
        return cc.messages

    @staticmethod
    def handle_citing_inactive_cc_no_button_reply(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """This is for the handling of a message from the user citing the CC when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body = f"User sent a free message citing the CC but it wasn't active"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_citing_active_cc_no_button_reply(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """This is for the handling of a message from the user citing the CC when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body="Continuous conversation ended because user sent a free message citing the CC"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_inactive_cc_rejected(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply rejecting the CC request when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.REJECTED)
        body="Continuous conversation rejected by the user but it wasn't active"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_active_cc_rejected(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply rejecting the CC request when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.REJECTED)
        body="Continuous conversation rejected by the user, not sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.ERROR, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc


    @staticmethod
    def handle_inactive_cc_accepted(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply accepting the CC request when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.APPROVED)
        body="Continuous conversation approved by the user but it wasn't active, not sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_active_cc_accepted(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply accepting the CC request when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.APPROVED)
        body="Continuous conversation approved by the user, sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.SUCCESS)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_forced_send_cc(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        cc.set_status(status=ContinuousConversationStatus.FORCED_SENT)
        body="Sending Continuous Conversation messages because it was forced to be sent and user opened the free conversation back again"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.SUCCESS)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc

    @staticmethod
    def handle_active_cc_non_related_message(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """If we eventually want to apply NLP to detect if the message is related to a CC (if there's an active CC, here's where we'll do it)"""
        ###Here we need to add that if its a forced_send, we send the messages anyway
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body="Continuous conversation ended because user sent a free message (not a button reply)"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=cc.calls_to_action)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        chat.add_central_notification(central_notif)
        return cc