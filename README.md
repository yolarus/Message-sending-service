# Курсовая работа №4, модуль 7

## Описание
1. Настроен полный CBV CRUD для моделей Message, Recipient, Mailing для каждого представления собраны шаблоны.
2. Для модели Mailing реализована отправка через интерфейс приложения и с помощью кастомной команды по id 'python manage.py send_mailing {id}'.
3. При отправке рассылки автоматически создается экземпляр попытки отправки AttemptMailing.
4. Реализована возможность регистрации пользователей в приложении с последующей верификацией через отправленную на почту ссылку.
5. Реализована возможность сброса пароля пользователя через email.
6. Создана группа пользователей Managers с уникальными правами mailings.can_disable_mailing, users.can_block_user. 
7. Доступ к редактированию страниц сообщений, получателей, рассылок, а также профиля пользователя открыт только для их владельцев и суперпользователя. 
8. Члены Managers имеют право только просматривать страницы из пункта выше, а также изменять статус рассылки или заблокировать пользователя (кроме суперпользователя).
9. На страницах со списками объектов отображаются только объекты владельцев, менеджеры и суперпользователи видят все объекты.
10. Все лишние кнопки убираются автоматически в шаблонах.
11. Неавторизованным пользователям закрыт ко всем страницам кроме главной.
12. На главной странице представлена общая статистика всего сервиса, а также имеется ссылка на страницу статистики конкретного пользователя. 
13. Настроено кеширование списков объектов mailings, recipients, users - данные queryset'ы используются как в ListView, так и в других сервисных функциях для оптимизации работы приложения. 
14. Выполнена проверка с помощью линтера flake8.
15. Создана кастомная команда 'python manage.py start-scheduler' для автоматической отправки сообщений по расписанию 
16. Созданы кастомные команды 'python manage.py load_mailings' и 'python manage.py load_users_groups_and_permissions' для заполнения БД
17. Настроены логирование всего проекта в файл log/main.log 
18. Создан файл README.md.

## Установка проекта
1. Клонирование проекта из [GitHub](https://github.com/yolarus/course_work_4) по HTTPS-токену или SSH-ключу.
2. Создание и заполнение файла .env своими данными.

## Установка зависимостей
1. Перейти в настройки Pycharm -> Setting -> Project -> Python Interpreter.
2. Добавить локальный интерпретатор с менеджером пакетов Poetry.
3. Выполнить команду в терминале PyCharm 'poetry install'.
4. Установить брокер Redis.

## Запуск
1. Запустить Redis, прописав в командной строке 'redis-server'. 
2. Прописать в командной строке 'python manage.py load_users_groups_and_permissions'. 
3. Прописать в командной строке 'python manage.py load_mailings'. 
4. Прописать в командной строке 'python manage.py runserver'. 
5. Нажать на ссылку на локальный сервер.

## Тестирование
1. Тесты не выполнялись.