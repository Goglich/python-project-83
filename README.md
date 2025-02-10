### Hexlet tests and linter status:
[![Actions Status](https://github.com/Goglich/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Goglich/python-project-83/actions)

https://python-project-83-owvd.onrender.com/

Page Analyzer - это веб приложение, построенное на основе Flask, которое позволяет анализировать указанные страницы на SEO-пригодность.


## Системные требования
- python 3.10+
- uv
- git


## Установка

Склонируйте репозиторий:

```bash
git clone git@github.com:Goglich/python-project-83.git
cd python-project-83
```

Выполните установку:

```bash
make install
```

Создайте .env файл окружения. Он должен содержать:

Секретный ключ:
SECRET_KEY=вашскекретныйключ

Строка для подключения к базе данных:
DATABASE_URL="postgresql://user:password@localhost:port/dbname"

## Сборка

Чтобы собрать проект, выполните:

```bash
export DATABASE_URL="ваша строка для подключения к БД"
``` 

```bash
make build
```

## Линтинг

Чтобы проверить код с помощью Flake8, выполните:

```bash
make lint
```

## Разработка

Для запуска сервера разработки Flask выполните:

```bash
make dev
```

Сервер будет запущен на `http://127.0.0.1:5000`.

## Запуск в продакшене

Для запуска приложения в продакшене с использованием Gunicorn выполните:

```bash
make start
```

По умолчанию сервер будет доступен на `http://0.0.0.0:8000`. Вы можете изменить порт, задав переменную окружения `PORT`:

```bash
make start PORT=5000
```