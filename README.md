# Тестовое задание для ООО "Технезис"

## Реализация тг-бота по парсингу данных с сайтов
[@TechnezisTestBot](https://t.me/TechnezisTestBot)

### Стек технологий
- ЯП Python 3.11
- Библиотека Aiogram 3.18
- БД Sqlite
- Инфраструктура Docker & docker-compose

### Структура проекта
- bot.py - основной файл для работы с тг-ботом
- keyboards.py - файл с клавиатурами тг-бота
- db.py - логика для работы с БД
- parser.py - логика парсинга цен с сайтов
- env.example - образец env файла с переменными окружения
- requirements.txt - зависимости
- Dockerfile - Dockerfile для контейнеризации
- docker-compose.yml - Docker Compose для запуска
- README.md - описание проекта и инструкция по развертыванию
- тест.xlsx - образец Excel-файла (современный формат)
- тест2.xls - образец Excel-файл (старый формат)

### Деплой проекта
1. Необходим установленный git и Docker на ОС
2. Склонируйте репозиторий в нужную папку
```commandline
git clone https://github.com/ptica41/Technezis.git
```
3. Перейдите в папку проекта
```commandline
cd Technezis
```
4. Cоздайте .env файл (скопируйте .env.example)
5. Запустите проект
```commandline
docker-compose up -d --build
```

### Описание проекта
При запуске бота [@TechnezisTestBot](https://t.me/TechnezisTestBot) 
командой */start* появляется кнопка "Загрузить файл", 
необходимо прикрепить файл xls/xlsx формата, происходит проверка валидности структуры файла,
для примера в репозитории представлены файлы с нужной структурой. 
Также происходит проверка на отправку файлов других форматов и текстовых данных 

При первой отправке валидного файла создаются БД sqlite и папка data, в которой будут храниться загруженные файлы.

Происходит запись данных в БД, парсинг данных с ценами и высчитывание среднего арифметического цен.
Данные отправляются пользователю тг-бота
