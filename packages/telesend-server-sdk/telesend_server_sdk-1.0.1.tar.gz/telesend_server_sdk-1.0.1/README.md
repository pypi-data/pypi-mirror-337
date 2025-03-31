# Telesend Server SDK для Python

## Установка

```bash
pip install telesend
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
