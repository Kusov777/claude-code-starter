# Примеры команд для бота Prorabchik

## Базовые команды PowerShell

### Навигация
```
# Текущая папка
Get-Location

# Список файлов
Get-ChildItem
ls  # или короче

# Перейти в папку
Set-Location C:\Users\kusov
cd C:\Users\kusov

# Показать содержимое файла
Get-Content README.md
cat README.md
```

### Информация о системе
```
# Кто я?
whoami

# Версия Windows
[System.Environment]::OSVersion

# Информация о ПК
Get-ComputerInfo

# Диски
Get-Volume

# Процессы
Get-Process
Get-Process | Select-Object Name, Memory | Sort-Object Memory -Descending
```

### Работа с файлами
```
# Создать папку
New-Item -Path "test_folder" -ItemType Directory
mkdir new_folder

# Создать файл
New-Item -Path "test.txt" -ItemType File

# Удалить файл
Remove-Item test.txt

# Копировать
Copy-Item source.txt dest.txt

# Переместить
Move-Item old.txt new.txt

# Размер папки
(Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
```

## Python команды

```
# Версия Python
python --version

# Список установленных пакетов
pip list

# Быстрый скрипт
python -c "print('Hello from bot!')"

# Запустить файл
python script.py

# Установить пакет
pip install requests
```

## Git команды

```
# Статус
git status

# Последние коммиты
git log --oneline -10

# Текущая ветка
git branch

# Создать ветку
git checkout -b new-feature

# Добавить файлы
git add .

# Коммит
git commit -m "message"

# Отправить
git push
```

## Node.js команды

```
# Версия Node
node --version
npm --version

# Установить пакеты
npm install

# Запустить скрипт
npm run dev

# Список скриптов
npm run
```

## Docker команды

```
# Список контейнеров
docker ps

# Запустить контейнер
docker run -d nginx

# Остановить
docker stop container_id

# Логи
docker logs container_id
```

## Полезные комбинации

```
# Поиск файлов
Get-ChildItem -Path "C:\" -Recurse -Filter "*.log" 2>$null

# Размер всех папок
Get-ChildItem -Directory | ForEach-Object { [PSCustomObject]@{Name=$_.Name; Size=$((Get-ChildItem $_ -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)} }

# Переменные окружения
[System.Environment]::GetEnvironmentVariables()

# История команд PowerShell
Get-History | Select-Object CommandLine, StartExecutionTime
```

## Советы

- 🔍 **Поиск в истории**: Используй `| grep` или `| Where-Object`
- ⏱️ **Долгие команды**: Добавь таймаут 120+ секунд если нужно
- 📊 **Форматирование**: Используй `| Format-Table`, `| Format-List`
- 💾 **Сохранить результат**: `Get-Process | Out-File processes.txt`

## Безопасные команды

Безопасны для выполнения через бота:

✅ Чтение файлов
✅ Просмотр процессов
✅ Проверка статуса
✅ Получение информации о системе
✅ Git команды
✅ Создание временных файлов

❌ Удаление файлов (особенно `/s`)
❌ Форматирование дисков
❌ Выключение/перезагрузка
❌ Изменение прав доступа
❌ Установка системных обновлений
