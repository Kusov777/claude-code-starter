"""
Конфигурация Telegram бота Prorabchik
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота (получишь от BotFather в Telegram)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# ID пользователя, которому разрешено управлять ботом (для безопасности)
ALLOWED_USER_ID = int(os.getenv('ALLOWED_USER_ID', '0'))

# Таймаут на выполнение команды (в секундах)
COMMAND_TIMEOUT = int(os.getenv('COMMAND_TIMEOUT', '30'))

# Максимальная длина сообщения в Telegram (4096 символов)
MAX_MESSAGE_LENGTH = 4096

# Запрещенные команды (для безопасности)
FORBIDDEN_COMMANDS = [
    'rm -rf',
    'format',
    'del /s',
    'shutdown',
    'restart',
]
