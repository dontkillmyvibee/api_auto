# api-auto

Тренировочный фреймворк для автоматизации тестирования REST API на Python.

## Стек

- **pytest** — тест-раннер
- **requests** — HTTP-клиент
- **SQLAlchemy 2.0** / **psycopg 3** — клиент к PostgreSQL для верификации данных
- **confluent-kafka** — клиент Kafka для проверки событий
- **pydantic** / **pydantic-settings** — схемы и конфигурация
- **allure-pytest** — отчёты
- **uv** — управление зависимостями и окружением
- **ruff** / **mypy** — линтинг, форматирование и статическая типизация

## Установка

Требуется [uv](https://docs.astral.sh/uv/) и Python 3.13+.

```bash
uv sync                     # установить зависимости из uv.lock
uv run pre-commit install   # включить git-хук (запускается сам на каждый commit)
```

`pre-commit install` нужно выполнить один раз после клонирования: git-хуки
не хранятся в репозитории, поэтому ставим хук локально))

### Доступ к Kafka с хоста

Тесты подключаются к **host-listener** Kafka: `localhost:9093` (не `9092` —
тот порт для контейнеров внутри Docker). В `docker-compose` у сервиса `kafka`
должен быть проброс:

```yaml
ports:
  - "9092:9092"   # для контейнеров (внутренняя сеть)
  - "9093:9093"   # для тестов с хоста
```

После добавления порта пересоздай контейнер: `docker compose up -d kafka`.

## Запуск

```bash
uv run pytest                      # прогнать тесты
LOG_LEVEL=DEBUG uv run pytest      # с детальным логированием
uv run ruff check .                # линтинг
uv run ruff format .               # форматирование
uv run mypy .                      # проверка типов
```

Отчёт Allure:

```bash
uv run pytest
allure serve allure-results
```
