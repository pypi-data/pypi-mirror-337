from typing import List, Optional, Union, Literal

class Button:
    """Button for Telegram keyboard"""
    def __init__(
        self,
        text: str,
        url: Optional[str] = None,
        callback_data: Optional[str] = None
    ):
        self.text = text
        self.url = url
        self.callback_data = callback_data
    
    def to_dict(self):
        """Converts the object to a dictionary for API"""
        result = {"text": self.text}
        if self.url:
            result["url"] = self.url
        if self.callback_data:
            result["callback_data"] = self.callback_data
        return result

class MediaItem:
    """Media item for media group"""
    def __init__(
        self,
        type: Literal['audio', 'document', 'photo', 'video'],
        url: str,
        caption: Optional[str] = None
    ):
        self.type = type
        self.url = url
        self.caption = caption
    
    def to_dict(self):
        """Converts the object to a dictionary for API"""
        result = {
            "type": self.type,
            "media": self.url
        }
        if self.caption:
            result["caption"] = self.caption
        return result

class BaseMessage:
    """Base class for all message types"""
    def __init__(
        self,
        disable_notification: bool = False,
        parse_mode: Optional[str] = None
    ):
        self.disable_notification = disable_notification
        self.parse_mode = parse_mode

class MessageText(BaseMessage):
    """Text message"""
    def __init__(
        self,
        text: str,
        buttons: Optional[List[Button]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[str] = None
    ):
        super().__init__(disable_notification, parse_mode)
        self.type = "message"
        self.text = text
        self.buttons = buttons or []

class MessageMediaGroup(BaseMessage):
    """Media group message"""
    def __init__(
        self,
        items: List[MediaItem],
        disable_notification: bool = False
    ):
        super().__init__(disable_notification)
        self.type = "mediaGroup"
        self.items = items

class MessagePhoto(BaseMessage):
    """Photo message"""
    def __init__(
        self,
        photo: str,
        caption: Optional[str] = None,
        buttons: Optional[List[Button]] = None,
        disable_notification: bool = False,
        parse_mode: Optional[str] = None
    ):
        super().__init__(disable_notification, parse_mode)
        self.type = "photo"
        self.photo = photo
        self.caption = caption
        self.buttons = buttons or []

class MessageVideoNote(BaseMessage):
    """Video note message"""
    def __init__(
        self,
        video_note: str,
        buttons: Optional[List[Button]] = None,
        disable_notification: bool = False
    ):
        super().__init__(disable_notification)
        self.type = "videoNote"
        self.video_note = video_note
        self.buttons = buttons or []

class MessageVoice(BaseMessage):
    """Voice message"""
    def __init__(
        self,
        voice: str,
        caption: Optional[str] = None,
        disable_notification: bool = False,
        parse_mode: Optional[str] = None
    ):
        super().__init__(disable_notification, parse_mode)
        self.type = "voice"
        self.voice = voice
        self.caption = caption

class MessagePoll(BaseMessage):
    """Poll message"""
    def __init__(
        self,
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        allows_multiple_answers: bool = False,
        disable_notification: bool = False
    ):
        super().__init__(disable_notification)
        self.type = "poll"
        self.question = question
        self.options = options
        self.is_anonymous = is_anonymous
        self.allows_multiple_answers = allows_multiple_answers

TelegramMessage = Union[
    MessageText,
    MessageMediaGroup,
    MessagePhoto,
    MessageVideoNote,
    MessageVoice,
    MessagePoll
]
