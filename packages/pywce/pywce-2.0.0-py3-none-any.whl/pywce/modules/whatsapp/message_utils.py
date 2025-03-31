import json
from typing import Dict, Any

from pywce.modules.whatsapp.model import MessageTypeEnum, ResponseStructure


class MessageUtils:
    _TYPE_MAPPING: Dict = {
        "text": MessageTypeEnum.TEXT,
        "button": MessageTypeEnum.BUTTON,
        "image": MessageTypeEnum.IMAGE,
        "document": MessageTypeEnum.DOCUMENT,
        "video": MessageTypeEnum.VIDEO,
        "audio": MessageTypeEnum.AUDIO,
        "reaction": MessageTypeEnum.REACTION,
        "unknown": MessageTypeEnum.UNKNOWN,
        "unsupported": MessageTypeEnum.UNSUPPORTED,
        "order": MessageTypeEnum.ORDER,
        "interactive": MessageTypeEnum.INTERACTIVE,
        "sticker": MessageTypeEnum.STICKER,

        # interactive inner types
        "list_reply": MessageTypeEnum.INTERACTIVE_LIST,
        "button_reply": MessageTypeEnum.INTERACTIVE_BUTTON,
        "nfm_reply": MessageTypeEnum.INTERACTIVE_FLOW,
    }

    def __init__(self, message_data: Dict[str, Any]):
        self.message_data = message_data

    def get_structure(self) -> ResponseStructure:
        """
        parse message data and return type(model) and the response type data

        :return: ResponseStructure
        """
        message_type = self.message_data.get("type")

        if "location" in self.message_data:
            return ResponseStructure(typ=MessageTypeEnum.LOCATION, body=self.message_data.get("location"))

        if "contacts" in self.message_data:
            return ResponseStructure(typ=MessageTypeEnum.CONTACTS, body=self.message_data.get("contacts"))

        type_ = self._TYPE_MAPPING.get(message_type, MessageTypeEnum.UNKNOWN)

        if type_ == MessageTypeEnum.INTERACTIVE:
            inner_type = self.message_data.get("interactive").get("type")
            type_ = self._TYPE_MAPPING.get(
                inner_type,
                MessageTypeEnum.INTERACTIVE
            )

            if type_ is not MessageTypeEnum.INTERACTIVE:
                if inner_type == "nfm_reply":
                    response: Dict = self.message_data.get("interactive").get(inner_type)
                    return ResponseStructure(typ=type_, body=json.loads(response.get("response_json")))

                return ResponseStructure(typ=type_, body=self.message_data.get("interactive").get(inner_type))

            return ResponseStructure(typ=type_, body=self.message_data.get("interactive"))

        return ResponseStructure(typ=type_, body=self.message_data.get(message_type))
