from typing import Dict, Any, List, Optional, Callable
from .broadcast import UserData, MessageQueueItem

class UserDetails:
    """User details for identification"""
    def __init__(
        self,
        id: str,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_premium: Optional[bool] = None,
        time_zone: Optional[int] = None
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_premium = is_premium
        self.time_zone = time_zone
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the object to a dictionary for API"""
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'isPremium': self.is_premium,
            'timeZone': self.time_zone
        }

class Event:
    """Analytics event"""
    def __init__(
        self,
        start_parameter: str,
        path: str,
        params: Dict[str, Any],
        language: Optional[str] = None,
        device: Optional[str] = None
    ):
        self.start_parameter = start_parameter
        self.path = path
        self.params = params
        self.language = language
        self.device = device or "sdk"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the object to a dictionary for API"""
        return {
            'startParameter': self.start_parameter,
            'path': self.path,
            'params': self.params,
            'language': self.language,
            'device': self.device
        }

class TelesendClientConfig:
    """Telesend client configuration"""
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        migrate_users_hook: Optional[Callable[[], List[UserData]]] = None,
        callback_hook_send_message: Optional[Callable[[MessageQueueItem], None]] = None
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://api.telesend.io"
        self.migrate_users_hook = migrate_users_hook
        self.callback_hook_send_message = callback_hook_send_message
