from typing import Optional, Dict

class ApiConfigResponse:
    """API response with configuration"""
    def __init__(self, rabbitmq: Optional[Dict[str, str]] = None):
        self.rabbitmq = rabbitmq
        
    @classmethod
    def from_dict(cls, data: Dict):
        """Creates object from dictionary received from API"""
        return cls(
            rabbitmq=data.get('rabbitmq')
        )
