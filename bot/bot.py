"""
Telegram бот Prorabchik - выполняет команды из терминала
"""
import logging
import subprocess
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, ALLOWED_USER_ID, COMMAND_TIMEOUT, MAX_MESSAGE_LENGTH, FORBIDDEN_COMMANDS

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def is_user_allowed(user_id: int) -> bool:
    """Проверяет, разрешен ли пользователь"""
    return user_id == ALLOWED_USER_ID


def is_command_safe(command: str) -> bool:
    """Проверяет, безопасна ли команда"""
    command_lower = command.lower()
    for forbidden in FORBIDDEN_COMMANDS:
        if forbidden.lower() in command_lower:
            return False
    return True


async def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH):
    """Разбивает длинный текст на части"""
    for i in range(0, len(text), max_length):
        yield text[i:i + max_length]


async def execute_command(command: str) -> tuple[bool, str]:
    """
    Выполняет команду в терминале
    Возвращает (успех, вывод)
    """
    try:
        # Используем PowerShell для Windows
        result = subprocess.run(
            ['powershell', '-Command', command],
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT
        )
        
        output = result.stdout + result.stderr
        success = result.returncode == 0
        
        if not output:
            output = "✓ Команда выполнена успешно (вывода нет)"
        
        return success, output
    
    except subprocess.TimeoutExpired:
        return False, f"❌ Ошибка: команда выполнялась дольше {COMMAND_TIMEOUT} секунд"
    except Exception as e:
        return False, f"❌ Ошибка выполнения: {str(e)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ У вас нет доступа к этому боту")
        return
    
    welcome_text = """
🤖 Привет! Я бот **Prorabchik**

Я выполняю команды в терминале и отправляю результаты.

**Доступные команды:**
/help - справка
/start - этот текст

**Просто отправь мне команду**, например:
`dir` - вывести содержимое папки
`python --version` - проверить версию Python
`whoami` - узнать текущего пользователя

⚠️ Некоторые опасные команды заблокированы для безопасности
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ У вас нет доступа к этому боту")
        return
    
    help_text = """
**Как использовать этого бота:**

1. **Отправи команду** в чат
2. Бот выполнит её в PowerShell
3. Получишь результат

**Примеры:**
- `Get-Location` - текущая папка
- `Get-Process` - список процессов
- `python -c "print('Hello')"` - выполнить Python код
- `git status` - статус репозитория

**Ограничения:**
- Максимум 30 секунд на выполнение
- Сообщения обрезаются на 4096 символов
- Опасные команды заблокированы

**Безопасность:**
Бот может выполнять только пользователь с ID: {0}
"""
    await update.message.reply_text(help_text.format(ALLOWED_USER_ID), parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений (команды)"""
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ У вас нет доступа к этому боту")
        return
    
    command = update.message.text.strip()
    
    # Проверяем безопасность
    if not is_command_safe(command):
        await update.message.reply_text(
            "❌ Эта команда запрещена по соображениям безопасности"
        )
        return
    
    # Показываем, что обрабатываем
    status_msg = await update.message.reply_text(f"⏳ Выполняю: `{command}`", parse_mode='Markdown')
    
    # Выполняем команду
    success, output = await execute_command(command)
    
    # Форматируем результат
    if success:
        result_text = f"✅ **Успешно**\n\n```\n{output}\n```"
    else:
        result_text = f"❌ **Ошибка**\n\n```\n{output}\n```"
    
    # Если результат слишком длинный, разбиваем на части
    message_parts = []
    async for part in split_message(result_text):
        message_parts.append(part)
    
    # Удаляем статус и отправляем результаты
    try:
        await status_msg.delete()
    except:
        pass
    
    for part in message_parts:
        await update.message.reply_text(part, parse_mode='Markdown')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    try:
        await update.message.reply_text(f"❌ Произошла ошибка: {str(context.error)}")
    except:
        pass


def main():
    """Запуск бота"""
    if TELEGRAM_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Не установлен TELEGRAM_TOKEN в переменных окружения!")
        print("Как установить:")
        print("1. Создай файл .env в папке bot/")
        print("2. Добавь строку: TELEGRAM_TOKEN=your_token_here")
        print("3. Получи токен от @BotFather в Telegram")
        return
    
    if ALLOWED_USER_ID == 0:
        logger.error("❌ Не установлен ALLOWED_USER_ID в переменных окружения!")
        print("Как установить:")
        print("1. Найди свой ID в @userinfobot")
        print("2. Добавь в .env: ALLOWED_USER_ID=your_id")
        return
    
    logger.info(f"🤖 Запускаю бот Prorabchik...")
    
    # Создаем приложение
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    app.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("🚀 Бот готов к работе!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
