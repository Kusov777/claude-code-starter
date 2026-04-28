@echo off
REM Автоматическая настройка и запуск бота Prorabchik

echo.
echo === Бот Telegram Prorabchik ===
echo.

REM Проверяем .env файл
if not exist ".env" (
    echo ❌ Ошибка: файл .env не найден!
    echo.
    echo Создайте .env файл на основе .env.example
    echo.
    pause
    exit /b 1
)

REM Проверяем токен
findstr /C:"TELEGRAM_TOKEN=" .env >nul
if errorlevel 1 (
    echo ❌ TELEGRAM_TOKEN не найден в .env
    pause
    exit /b 1
)

REM Проверяем ID пользователя
findstr /C:"ALLOWED_USER_ID=YOUR_USER_ID_HERE" .env >nul
if not errorlevel 1 (
    echo ⚠️  ALLOWED_USER_ID не настроен!
    echo.
    echo 🔍 Получаю ваш ID пользователя...
    echo 📱 Напишите любое сообщение боту в Telegram
    echo ⏹️  После получения ID закройте скрипт (Ctrl+C)
    echo.
    python get_user_id.py
    echo.
    echo ✏️  Теперь отредактируйте файл .env и замените YOUR_USER_ID_HERE на полученный ID
    echo.
    pause
    exit /b 1
)

echo ✓ Конфигурация проверена

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo Скачайте Python с https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python найден

REM Устанавливаем зависимости
echo.
echo ⏳ Устанавливаю зависимости...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✓ Зависимости установлены

REM Запускаем бота
echo.
echo 🚀 Запускаю бота Prorabchik...
echo 📱 Бот готов принимать команды из Telegram!
echo ⏹️  Для остановки нажмите Ctrl+C
echo.
python bot.py

pause

