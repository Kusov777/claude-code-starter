# Установка Claude плагина Telegram

## Вариант 1: Через Claude CLI (если установлен)

Выполните команды в PowerShell:

```powershell
# Установить плагин Telegram
/plugin install telegram@claude-plugins-official

# Перезагрузить плагины
/reload-plugins

# Настроить Telegram (добавьте ваш токен)
/telegram:configure 8554492200:AAFuWQ-bPnr5tFrLGeRmThYetLDiqaKyr3A
```

## Вариант 2: Ручная настройка в VS Code

Если CLI плагины не доступны:

1. **Откройте расширения VS Code** (`Ctrl+Shift+X`)
2. **Поиск**: "Claude Telegram"
3. **Установите** нужное расширение
4. **Перезагрузите** VS Code

## Вариант 3: Запустить бота напрямую

Наш бот уже готов работать! Просто запустите:

```powershell
cd c:\Users\kusov\.vscode\moy-proekt\bot
python bot.py
```

## Проверка

Когда бот запущен, в Telegram напишите боту:
- `/start` — приветствие
- `/help` — справка
- `Get-Process` — список процессов
- `dir` — содержимое папки

## Ошибки?

❌ **"TELEGRAM_TOKEN not set"**
→ Отредактируйте `bot/.env` и добавьте токен

❌ **"ALLOWED_USER_ID is 0"**
→ Напишите `@userinfobot`, узнайте ваш ID, добавьте в `bot/.env`

❌ **"ModuleNotFoundError"**
→ Переустановите зависимости:
```powershell
pip install -r bot/requirements.txt
```
