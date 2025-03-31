from typing import List, Union, Literal
from .messages import TelegramMessage

class UserData:
    """User data"""
    def __init__(self, tg: Union[str, int]):
        self.tg = tg
        
    def to_dict(self):
        """Converts the object to a dictionary for API"""
        return {"tg": str(self.tg)}

class BroadcastOptions:
    """Parameters for message broadcast"""
    def __init__(
        self,
        users: Union[List[str], Literal['all']],
        content: TelegramMessage
    ):
        self.users = users
        self.content = content

class MessageQueueItem:
    """Message queue item"""
    def __init__(self, user_id: str, message: TelegramMessage):
        self.user_id = user_id
        self.message = message
        
    def to_dict(self):
        """Converts the object to a dictionary for API"""
        return {
            "userId": self.user_id,
            "message": self._message_to_dict(self.message)
        }
    
    def _message_to_dict(self, message):
        """Converts message to dictionary for API"""
        message_dict = {k: v for k, v in message.__dict__.items() if not k.startswith('_')}
        
        if 'buttons' in message_dict and message_dict['buttons']:
            message_dict['buttons'] = [button.to_dict() for button in message_dict['buttons']]
            
        if 'items' in message_dict and message_dict['items']:
            message_dict['items'] = [item.to_dict() for item in message_dict['items']]
            
        return message_dict
