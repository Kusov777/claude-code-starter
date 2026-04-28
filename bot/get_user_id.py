"""
Скрипт для получения ID пользователя Telegram
Запустите этот скрипт, напишите боту в Telegram, и он покажет ваш ID
"""
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает ID пользователя"""
    user = update.effective_user
    user_id = user.id
    username = user.username or "без username"
    first_name = user.first_name or ""

    message = f"""
🎯 **Ваш ID пользователя Telegram:**

**ID:** `{user_id}`
**Имя:** {first_name}
**Username:** @{username}

➡️ Скопируйте этот ID и вставьте в файл `bot/.env` вместо `YOUR_USER_ID_HERE`

После этого можете закрыть этот скрипт (Ctrl+C) и запустить основной бот.
"""

    await update.message.reply_text(message, parse_mode='Markdown')

    # Логируем в консоль для удобства
    print(f"\n{'='*50}")
    print(f"ПОЛУЧЕН ID ПОЛЬЗОВАТЕЛЯ:")
    print(f"ID: {user_id}")
    print(f"Имя: {first_name}")
    print(f"Username: @{username}")
    print(f"{'='*50}\n")

def main():
    if not TELEGRAM_TOKEN:
        print("❌ Ошибка: TELEGRAM_TOKEN не найден в .env файле")
        return

    print("🤖 Запускаю скрипт получения ID...")
    print("📱 Напишите любое сообщение боту в Telegram")
    print("🔢 Бот ответит вашим ID")
    print("⏹️  После получения ID нажмите Ctrl+C для выхода")
    print()

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("\n✅ Скрипт остановлен")

if __name__ == '__main__':
    main()
