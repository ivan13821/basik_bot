# sseu-schedule-bot
Бот-игра для экономиство СГЭУ СГЭУ


# Запуск бота
Для запуска бота необходимо:
1. Создать бота в telegram, используя бота https://t.me/BotFather;
2. Запросить его API Token у https://t.me/BotFather;
3. Переименовать файл config.ini.default в config.ini;
4. Внутри файла config.ini: вставить токен из пункта 2 в поле api_token, раздела [telegram];
5. Внутри файла config.ini: В поле feedback_chat_id раздела [telegram] указать ID чата, куда будут сбрасываться сообщения из раздела меню "Помощь" (получить его можно если зарегистрироваться в боте);
6. Внутри файла config.ini: В поле frequency раздела [spam] указаьб возможную частоту обращения пользователя к боту


# Команды
- /game - начинает игру


# Настройка защиты от спама
Переменные в файле config.ini определяют правила блокировки пользователя.

Система не дает пользователю отправлять запросы чаще чем 0.5 раз в сек.
