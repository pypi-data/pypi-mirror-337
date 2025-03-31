# Telesend Server SDK для Python

## Установка

```bash
pip install telesend-server-sdk
```

## Быстрый старт

```python
from telesend.client import TelesendClient
from telesend.types import TelesendClientConfig, MessageText

config = TelesendClientConfig(
    api_key="ваш_api_ключ"
)

client = TelesendClient(config)

client.on_message_sent(lambda user_id, success: print(f"Сообщение для {user_id}: {'успешно' if success else 'неуспешно'}"))
client.on_error(lambda error: print(f"Ошибка: {error}"))
client.on_connected(lambda: print("Подключено к серверу"))
client.on_disconnected(lambda: print("Отключено от сервера"))
message = MessageText(
    text="Привет, мир!",
    parse_mode="HTML"
)

client.broadcast({
    "users": ["123456789"],
    "content": message
})
```

## Примеры сообщений

### Текстовое сообщение с кнопками

```python
from telesend.types import MessageText, Button

message = MessageText(
    text="Выберите опцию:",
    buttons=[
        Button(text="Опция 1", callback_data="option_1"),
        Button(text="Опция 2", callback_data="option_2")
    ],
    parse_mode="HTML"
)
```

### Фото сообщение

```python
from telesend.types import MessagePhoto

message = MessagePhoto(
    photo="https://example.com/image.jpg",
    caption="Описание изображения",
    parse_mode="HTML"
)
```

### Группа медиа

```python
from telesend.types import MessageMediaGroup, MediaItem

message = MessageMediaGroup(
    items=[
        MediaItem(type="photo", url="https://example.com/image1.jpg"),
        MediaItem(type="photo", url="https://example.com/image2.jpg", caption="Описание второго фото")
    ]
)
```

## Использование callback для отправки сообщений в Telegram

```python
import requests
import json
from telesend.client import TelesendClient, compose_message
from telesend.types import TelesendClientConfig, MessageQueueItem

# Функция для отправки сообщения в Telegram
async def send_telegram_message(message_data: MessageQueueItem):
    user_id = message_data.user_id
    message = message_data.message
    
    base_url = f"https://api.telegram.org/botYOUR_BOT_TOKEN"
    
    # Преобразуем сообщение в формат, понятный Telegram API
    message_format = compose_message(message_data)
    
    # Отправляем запрос к API Telegram
    method = message_format["type"]
    payload = message_format["body"]
    
    response = requests.post(f"{base_url}/{method}", json=payload)
    
    if not response.ok:
        error_msg = f"Failed to send message: {response.status_code} {response.text}"
        print(error_msg)
        raise Exception(error_msg)
    
    print(f"Message sent to user {user_id}")
    return response.json()

# Создаем конфигурацию с callback'ом
config = TelesendClientConfig(
    api_key="YOUR_API_KEY",
    callback_hook_send_message=send_telegram_message
)

client = TelesendClient(config)
```

## Полный пример

```python
import time
from telesend.client import TelesendClient
from telesend.types import TelesendClientConfig, MessageText, BroadcastOptions

# Создание конфигурации
config = TelesendClientConfig(
    api_key="ваш_api_ключ"
)

# Инициализация клиента
client = TelesendClient(config)

# Подписка на события
client.on_message_sent(lambda user_id, success: print(f"Сообщение для {user_id}: {'успешно' if success else 'неуспешно'}"))
client.on_error(lambda error: print(f"Ошибка: {error}"))
client.on_connected(lambda: print("Подключено к серверу"))
client.on_disconnected(lambda: print("Отключено от сервера"))

# Ожидание подключения
time.sleep(2)

# Создание текстового сообщения
message = MessageText(
    text="Привет! Это тестовое сообщение от <b>Telesend Server SDK</b>",
    parse_mode="HTML"
)

# Создание опций для рассылки
broadcast_options = BroadcastOptions(
    users=["123456789"],  # ID пользователей Telegram
    content=message
)

# Отправка сообщения
result = client.broadcast(broadcast_options)
if result:
    print(f"Сообщение отправлено, ID рассылки: {result['broadcastId']}")
else:
    print("Не удалось отправить сообщение")

# Ожидание обработки сообщений
time.sleep(5)

# Закрытие клиента в конце работы программы
client.close()
