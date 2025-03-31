import json
import time
import threading
import logging
from typing import Dict, Any, Optional, List, Set, Callable, Union, Tuple
import pika
import requests
from .types.events import Event, UserDetails, TelesendClientConfig
from .types.broadcast import BroadcastOptions, MessageQueueItem, UserData
from .types.messages import (
    Button, MessageText, MessageMediaGroup, MessagePhoto, 
    MessageVideoNote, MessageVoice, MessagePoll, TelegramMessage
)
from .types.api import ApiConfigResponse

logger = logging.getLogger("telesend")

def compose_message(message_data: MessageQueueItem) -> Dict[str, Any]:
    """
    Composes message for sending to Telegram API
    
    Args:
        message_data: Message data
        
    Returns:
        Prepared type and body of the request
    """
    user_id = message_data.user_id
    message = message_data.message
    message_type = ""
    body = {}
    
    if isinstance(message, MessageText):
        message_type = "sendMessage"
        body = {
            "chat_id": user_id,
            "text": message.text,
            "parse_mode": message.parse_mode,
            "disable_notification": message.disable_notification
        }
        
        if message.buttons and len(message.buttons) > 0:
            buttons_dict = [button.to_dict() for button in message.buttons]
            body["reply_markup"] = {
                "inline_keyboard": [buttons_dict]
            }
            
    elif isinstance(message, MessagePhoto):
        message_type = "sendPhoto"
        body = {
            "chat_id": user_id,
            "photo": message.photo,
            "caption": message.caption,
            "parse_mode": message.parse_mode,
            "disable_notification": message.disable_notification
        }
        
        if message.buttons and len(message.buttons) > 0:
            buttons_dict = [button.to_dict() for button in message.buttons]
            body["reply_markup"] = {
                "inline_keyboard": [buttons_dict]
            }
            
    elif isinstance(message, MessageVideoNote):
        message_type = "sendVideoNote"
        body = {
            "chat_id": user_id,
            "video_note": message.video_note,
            "disable_notification": message.disable_notification
        }
            
    elif isinstance(message, MessageVoice):
        message_type = "sendVoice"
        body = {
            "chat_id": user_id,
            "voice": message.voice,
            "caption": message.caption,
            "parse_mode": message.parse_mode,
            "disable_notification": message.disable_notification
        }
            
    elif isinstance(message, MessagePoll):
        message_type = "sendPoll"
        body = {
            "chat_id": user_id,
            "question": message.question,
            "options": message.options,
            "is_anonymous": message.is_anonymous,
            "allows_multiple_answers": message.allows_multiple_answers,
            "disable_notification": message.disable_notification
        }
            
    elif isinstance(message, MessageMediaGroup):
        message_type = "sendMediaGroup"
        media = [item.to_dict() for item in message.items]
        
        body = {
            "chat_id": user_id,
            "media": media,
            "disable_notification": message.disable_notification
        }
    
    else:
        raise ValueError(f"Unsupported message type: {type(message)}")
        
    return {"type": message_type, "body": body}


class TelesendClient:
    """
    Client for interacting with Telesend service
    """
    QUEUE_PREFIX = "broadcast_"
    BATCH_SIZE = 20
    BATCH_INTERVAL = 1.0
    MAX_RECONNECT_ATTEMPTS = 10
    
    def __init__(self, config: TelesendClientConfig):
        """
        Creates a new Telesend client instance
        
        Args:
            config: Client configuration
        """
        self.api_key = config.api_key
        self.base_url = config.base_url
        self.migrate_users_hook = config.migrate_users_hook
        self.callback_hook_send_message = config.callback_hook_send_message
        
        self.active_broadcasts: Set[str] = set()
        self.connection = None
        self.channel = None
        self.processing_messages = False
        self.consumer_tag = None
        self.reconnect_attempts = 0
        self.reconnect_timer = None
        self.process_incomplete_timer = None
        self.last_batch_time = 0
        self.is_connecting = False
        self.connection_url = ""
        self.should_reconnect = False
        self.was_connected = False
        
        self.message_sent_callbacks = []
        self.error_callbacks = []
        self.connected_callbacks = []
        self.disconnected_callbacks = []
        
        threading.Thread(target=self._setup_config).start()
        
    def _setup_config(self) -> None:
        """
        Retrieves configuration from API and sets connection parameters
        """
        max_retries = 3
        retries = 0
        success = False
        
        while retries < max_retries and not success:
            try:
                if retries > 0:
                    self._emit_info(f"Getting configuration, attempt: {retries + 1} of {max_retries}")
                    time.sleep(5)
                
                response = self._make_request('/api/sdk/config', 'GET')
                config_data = response
                config = ApiConfigResponse.from_dict(config_data)
                
                if config.rabbitmq and 'url' in config.rabbitmq:
                    self.connection_url = config.rabbitmq['url']
                else:
                    self.connection_url = 'amqp://localhost'
                
                success = True
                self._connect_to_rabbitmq()
            except Exception as error:
                retries += 1
                if retries >= max_retries:
                    self.connection_url = 'amqp://localhost'
                    self._emit_error(f"Failed to get configuration from API after {max_retries} attempts: {str(error)}. Using default connection.")
                    self._connect_to_rabbitmq()
                else:
                    self._emit_warn(f"Error getting configuration (attempt {retries} of {max_retries}): {str(error)}. Retrying in 5 seconds.")
    
    def _connect_to_rabbitmq(self) -> None:
        """
        Establishes connection with RabbitMQ
        """
        if self.is_connecting:
            return
        
        self.is_connecting = True
        
        try:
            parameters = pika.URLParameters(self.connection_url)
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            queue_name = f"{self.QUEUE_PREFIX}{self.api_key}"
            self.channel.queue_declare(queue=queue_name, durable=True)
            
            self.is_connecting = False
            self.reconnect_attempts = 0
            self.was_connected = True
            self._emit_connected()
            
            self._start_processing_messages()
            
            self._connection_monitor()
            
        except Exception as error:
            self.is_connecting = False
            self._emit_error(f"Failed to connect to RabbitMQ: {str(error)}")
            self._handle_disconnect()
    
    def _connection_monitor(self):
        """
        Monitors the connection state in a separate thread
        """
        def monitor_task():
            while self.connection and not self.connection.is_closed:
                time.sleep(5)
            
            if self.was_connected:
                self._on_connection_closed()
                
        monitor_thread = threading.Thread(target=monitor_task)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def _on_connection_closed(self):
        """Handler for connection closure"""
        self._emit_error(f"Connection to RabbitMQ closed")
        self._emit_disconnected()
        self._handle_disconnect()
    
    def _handle_disconnect(self) -> None:
        """
        Handles disconnection and attempts to reconnect
        """
        self._emit_disconnected()
        
        self.channel = None
        self.connection = None
        self.processing_messages = False
        self.consumer_tag = None
        
        self.reconnect_attempts += 1
        
        if self.reconnect_attempts <= self.MAX_RECONNECT_ATTEMPTS:
            delay = min(1000 * pow(2, self.reconnect_attempts - 1), 30000) / 1000.0
            
            if self.reconnect_timer:
                self.reconnect_timer.cancel()
            
            self.reconnect_timer = threading.Timer(delay, self._connect_to_rabbitmq)
            self.reconnect_timer.daemon = True
            self.reconnect_timer.start()
        else:
            self._emit_error(f"Failed to reconnect to RabbitMQ after {self.MAX_RECONNECT_ATTEMPTS} attempts")
    
    def _make_request(self, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes HTTP request to API
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Data to send
            
        Returns:
            Server response
        """
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        url = f"{self.base_url}{endpoint}"
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, json=data)
        
        if not response.ok:
            logger.error(f"Request not executed: {response.status_code} {response.text}")
            response.raise_for_status()
        
        return response.json()
    
    def _start_processing_messages(self) -> None:
        """
        Starts processing messages from queue
        """
        if not self.channel or self.processing_messages:
            return
        
        self.processing_messages = True
        queue_name = f"{self.QUEUE_PREFIX}{self.api_key}"
        
        self.channel.basic_qos(prefetch_count=self.BATCH_SIZE)
        
        processing_batch = []
        
        def process_message_callback(ch, method, _properties, body):
            """Message processing callback"""
            try:
                message_data = json.loads(body.decode('utf-8'))
                queue_item = MessageQueueItem(
                    user_id=message_data['userId'],
                    message=self._dict_to_message(message_data['message'])
                )
                
                processing_promise = threading.Thread(
                    target=self._process_queue_item,
                    args=(queue_item, ch, method)
                )
                processing_promise.daemon = True
                processing_promise.start()
                processing_batch.append(processing_promise)
                
                if len(processing_batch) >= self.BATCH_SIZE:
                    current_time = time.time()
                    if current_time - self.last_batch_time < self.BATCH_INTERVAL:
                        time.sleep(self.BATCH_INTERVAL - (current_time - self.last_batch_time))
                    
                    for thread in processing_batch:
                        thread.join()
                    
                    self.last_batch_time = time.time()
                    processing_batch.clear()
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.consumer_tag = queue_name
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=process_message_callback
        )
        
        threading.Thread(target=self.channel.start_consuming).start()
        
        def check_incomplete():
            if len(processing_batch) > 0:
                current_time = time.time()
                if current_time - self.last_batch_time < self.BATCH_INTERVAL:
                    time.sleep(self.BATCH_INTERVAL - (current_time - self.last_batch_time))
                
                for thread in processing_batch:
                    thread.join()
                
                self.last_batch_time = time.time()
                processing_batch.clear()
                
            if self.processing_messages:
                self.process_incomplete_timer = threading.Timer(0.5, check_incomplete)
                self.process_incomplete_timer.daemon = True
                self.process_incomplete_timer.start()
        
        self.process_incomplete_timer = threading.Timer(0.5, check_incomplete)
        self.process_incomplete_timer.daemon = True
        self.process_incomplete_timer.start()
    
    def _process_queue_item(self, message_data: MessageQueueItem, channel, method) -> None:
        """
        Processes a message from the queue
        
        Args:
            message_data: Message data
            channel: RabbitMQ channel
            method: Delivery method
        """
        try:
            if self.callback_hook_send_message:
                self.callback_hook_send_message(message_data)
            
            channel.basic_ack(delivery_tag=method.delivery_tag)
            self._emit_message_sent(message_data.user_id, True)
        except Exception as error:
            try:
                error_data = json.loads(str(error))
                if error_data.get('error_code') == 429:
                    queue_name = f"{self.QUEUE_PREFIX}{self.api_key}"
                    channel.basic_publish(
                        exchange='',
                        routing_key=queue_name,
                        body=json.dumps(message_data.to_dict()),
                        properties=pika.BasicProperties(
                            delivery_mode=2
                        )
                    )
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    self._emit_error(f"Request limit exceeded when sending message to user {message_data.user_id}, retry later")
                else:
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    self._emit_message_sent(message_data.user_id, False)
                    self._emit_error(f"Failed to send message to user {message_data.user_id}: {str(error)}")
            except json.JSONDecodeError:
                channel.basic_ack(delivery_tag=method.delivery_tag)
                self._emit_message_sent(message_data.user_id, False)
                self._emit_error(f"Failed to send message to user {message_data.user_id}: {str(error)}")
    
    def _stop_processing_messages(self) -> None:
        """
        Stops message processing
        """
        if not self.channel or not self.consumer_tag or not self.processing_messages:
            return
        
        if self.process_incomplete_timer:
            self.process_incomplete_timer.cancel()
            self.process_incomplete_timer = None
        
        if self.channel and self.consumer_tag:
            try:
                self.channel.basic_cancel(self.consumer_tag)
            except Exception:
                pass
        
        self.processing_messages = False
        self.consumer_tag = None
    
    def _dict_to_message(self, message_dict: Dict[str, Any]) -> TelegramMessage:
        """
        Converts dictionary to message object
        
        Args:
            message_dict: Dictionary with message data
            
        Returns:
            Message object of the appropriate type
        """
        message_type = message_dict.get('type')
        
        if message_type == 'message':
            buttons = None
            if 'buttons' in message_dict and message_dict['buttons']:
                buttons = [
                    Button(
                        text=btn.get('text', ''),
                        url=btn.get('url'),
                        callback_data=btn.get('callback_data')
                    ) for btn in message_dict['buttons']
                ]
            
            return MessageText(
                text=message_dict.get('text', ''),
                buttons=buttons,
                disable_notification=message_dict.get('disable_notification', False),
                parse_mode=message_dict.get('parse_mode')
            )
        
        elif message_type == 'photo':
            buttons = None
            if 'buttons' in message_dict and message_dict['buttons']:
                buttons = [
                    Button(
                        text=btn.get('text', ''),
                        url=btn.get('url'),
                        callback_data=btn.get('callback_data')
                    ) for btn in message_dict['buttons']
                ]
            
            return MessagePhoto(
                photo=message_dict.get('photo', ''),
                caption=message_dict.get('caption'),
                buttons=buttons,
                disable_notification=message_dict.get('disable_notification', False),
                parse_mode=message_dict.get('parse_mode')
            )
        
        elif message_type == 'videoNote':
            buttons = None
            if 'buttons' in message_dict and message_dict['buttons']:
                buttons = [
                    Button(
                        text=btn.get('text', ''),
                        url=btn.get('url'),
                        callback_data=btn.get('callback_data')
                    ) for btn in message_dict['buttons']
                ]
            
            return MessageVideoNote(
                video_note=message_dict.get('video_note', ''),
                buttons=buttons,
                disable_notification=message_dict.get('disable_notification', False)
            )
        
        elif message_type == 'voice':
            return MessageVoice(
                voice=message_dict.get('voice', ''),
                caption=message_dict.get('caption'),
                disable_notification=message_dict.get('disable_notification', False),
                parse_mode=message_dict.get('parse_mode')
            )
        
        elif message_type == 'poll':
            return MessagePoll(
                question=message_dict.get('question', ''),
                options=message_dict.get('options', []),
                is_anonymous=message_dict.get('is_anonymous', True),
                allows_multiple_answers=message_dict.get('allows_multiple_answers', False),
                disable_notification=message_dict.get('disable_notification', False)
            )
        
        elif message_type == 'mediaGroup':
            from .types.messages import MediaItem
            items = []
            
            if 'items' in message_dict and message_dict['items']:
                for item_dict in message_dict['items']:
                    items.append(
                        MediaItem(
                            type=item_dict.get('type', 'photo'),
                            url=item_dict.get('url', ''),
                            caption=item_dict.get('caption')
                        )
                    )
            
            return MessageMediaGroup(
                items=items,
                disable_notification=message_dict.get('disable_notification', False)
            )
        
        else:
            raise ValueError(f"Unsupported message type: {message_type}")
    
    def _emit_message_sent(self, user_id: str, success: bool) -> None:
        """Notifies about message sent"""
        for callback in self.message_sent_callbacks:
            try:
                callback(user_id, success)
            except Exception as e:
                logger.error(f"Error in messageSent callback: {str(e)}")
    
    def _emit_error(self, error_message: str) -> None:
        """Notifies about error"""
        error = Exception(error_message)
        logger.error(error_message)
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                logger.error(f"Error in error callback: {str(e)}")
    
    def _emit_info(self, info_message: str) -> None:
        """Logs informational message"""
        logger.info(info_message)
    
    def _emit_warn(self, warn_message: str) -> None:
        """Logs warning message"""
        logger.warning(warn_message)
    
    def _emit_connected(self) -> None:
        """Notifies about successful connection"""
        for callback in self.connected_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in connected callback: {str(e)}")
    
    def _emit_disconnected(self) -> None:
        """Notifies about disconnection"""
        for callback in self.disconnected_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in disconnected callback: {str(e)}")
    
    def on_message_sent(self, callback: Callable[[str, bool], None]) -> None:
        """
        Subscribes to message sent event
        
        Args:
            callback: Callback function, accepting user ID and success status
        """
        self.message_sent_callbacks.append(callback)
        return self
    
    def on_error(self, callback: Callable[[Exception], None]) -> None:
        """
        Subscribes to error event
        
        Args:
            callback: Callback function, accepting error object
        """
        self.error_callbacks.append(callback)
        return self
    
    def on_connected(self, callback: Callable[[], None]) -> None:
        """
        Subscribes to connection event
        
        Args:
            callback: Callback function
        """
        self.connected_callbacks.append(callback)
        return self
    
    def on_disconnected(self, callback: Callable[[], None]) -> None:
        """
        Subscribes to disconnection event
        
        Args:
            callback: Callback function
        """
        self.disconnected_callbacks.append(callback)
        return self
    
    def track(self, user_id: Union[str, int], event_type: str, payload: Event) -> None:
        """
        Sends analytics event
        
        Args:
            user_id: User ID
            event_type: Event type
            payload: Event data
        """
        payload_dict = payload.to_dict()
        language = payload_dict.pop('language', '')
        device = payload_dict.pop('device', 'sdk')
        
        self._make_request('/api/analytics/event', 'POST', {
            'eventType': event_type,
            'eventDetails': payload_dict,
            'telegramId': str(user_id),
            'language': language,
            'device': device
        })
    
    def identify(self, user: UserDetails) -> None:
        """
        Identifies user
        
        Args:
            user: User data
        """
        self._make_request('/api/analytics/identify', 'POST', user.to_dict())
    
    def is_connected(self) -> bool:
        """
        Checks if connection to RabbitMQ is established
        
        Returns:
            True if connection is established
        """
        return self.connection is not None and self.channel is not None
    
    def close(self) -> None:
        """
        Closes connections when the client is shutting down
        """
        if self.reconnect_timer:
            self.reconnect_timer.cancel()
            self.reconnect_timer = None
        
        self._stop_processing_messages()
        
        if self.channel:
            try:
                self.channel.close()
            except Exception:
                pass
        
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
    
    def broadcast(self, options: BroadcastOptions) -> Optional[Dict[str, str]]:
        """
        Creates a new broadcast
        
        Args:
            options: Broadcast parameters
            
        Returns:
            Information about the created broadcast or None in case of error
        """
        if not self.channel:
            logger.error("Connection not established")
            return None
        
        if options.users == 'all':
            if not self.migrate_users_hook:
                logger.error("migrate_users_hook required for broadcasting to all users")
                return None
            
            users = self.migrate_users_hook()
            user_ids = [str(u.tg) for u in users]
        else:
            user_ids = options.users
        
        broadcast_id = f"broadcast_{int(time.time())}_{str(int(time.time() * 1000))[-9:]}"
        queue_name = f"{self.QUEUE_PREFIX}{self.api_key}"
        
        for user_id in user_ids:
            message_item = MessageQueueItem(
                user_id=user_id,
                message=options.content
            )
            
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message_item.to_dict()),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
        
        self.active_broadcasts.add(broadcast_id)
        
        return {"broadcastId": broadcast_id}
