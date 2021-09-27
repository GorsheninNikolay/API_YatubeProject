API для социальной сети. API_YatubeProject
==

Данный проект представляет собой API, написанный по архитектуре REST API, для моего проекта YatubeProject.

Возможности:

- api/v1/api-token-auth/ (POST): передаём логин и пароль, получаем токен.

- api/v1/posts/ (GET, POST): получаем список всех постов или создаём новый пост.

- api/v1/posts/{post_id}/ (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем пост по id.

- api/v1/groups/ (GET): получаем список всех групп.

- api/v1/groups/{group_id}/ (GET): получаем информацию о группе по id.

- api/v1/posts/{post_id}/comments/ (GET, POST): получаем список всех комментариев поста с id=post_id или создаём новый, указав id поста, который хотим прокомментировать.

- api/v1/posts/{post_id}/comments/{comment_id}/ (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем комментарий по id у поста с id=post_id.

# Развертывание проекта

1. Зайдите в GitBash, при необходимости установите
2. При помощи команд 

Перейти в каталог:
```
cd "каталог"
```
Подняться на уровень вверх:
```
cd .. 
```
:exclamation: Перейдите в нужный каталог для клонирования репозитория :exclamation:

3. Клонирование репозитория:
```
git clone https://github.com/GorsheninNikolay/API_YatubeProject
```
4. Перейти в каталог:
```
cd API_YatubeProject
```
6. Создание виртуальной среды:
```
python -m venv venv 
```
5. Активация виртуальной среды:
```
source venv/Scripts/activate
```
6. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
7. Перейти в каталог:
```
cd yatube_api
```
8. Создать миграции:
```
python manage.py migrate
```
9. Запуск проекта:
```
python manage.py runserver
```

Готово! Можно отправлять запросы на ip адрес http://127.0.0.1:8000/ :wink:

Системные требования
----

- Python 3.7.3

- GitBash
