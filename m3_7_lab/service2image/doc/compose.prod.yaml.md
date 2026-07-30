# docker-compose.yml для прода

- [docker-compose.yml для прода](#docker-composeyml-для-прода)
  - [docker-compose](#docker-compose)
  - [Dockerfile](#dockerfile)
  - [Главные отличия продакшен-конфигурации от дебаг-версии](#главные-отличия-продакшен-конфигурации-от-дебаг-версии)
    - [1. Использование WSGI-сервера (Gunicorn вместо `flask run`)](#1-использование-wsgi-сервера-gunicorn-вместо-flask-run)
    - [2. Никаких volumes с исходным кодом](#2-никаких-volumes-с-исходным-кодом)
    - [3. Автоматический перезапуск (`restart: always`)](#3-автоматический-перезапуск-restart-always)
    - [4. Проверка состояния (`healthcheck`)](#4-проверка-состояния-healthcheck)
    - [5. Ротация логов (`logging`)](#5-ротация-логов-logging)
    - [Как это правильно запускать на сервере?](#как-это-правильно-запускать-на-сервере)
    - [изменить политику перезапуска](#изменить-политику-перезапуска)
      - [прямо у работающего или остановленного контейнера через CLI Docker](#прямо-у-работающего-или-остановленного-контейнера-через-cli-docker)
      - [Изменить в compose](#изменить-в-compose)
      - [Быстрая проверка политики](#быстрая-проверка-политики)

Для прод-окружения подход коренным образом меняется. Всё, что мы городили для отладки (монтирование исходников через `bind mounts`, `debugpy`, встроенный сервер Flask `Werkzeug`, открытые порты для debugger'а), в продакшене **строго запрещено** из соображений безопасности и производительности.

## docker-compose

Вот каким должен быть **`docker-compose.prod.yml`** (или `docker-compose.yml` для прода):

```yaml

services:
  learnpython:
    build:
      context: .
      dockerfile: Dockerfile
    image: service2image-prod
    container_name: service2image-prod
    restart: on-failure
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    ports:
      - "5002:5002"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5002/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Dockerfile

```Dockerfile
FROM python:3-slim

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "--threads", "2", "app:app"]

```

---

## Главные отличия продакшен-конфигурации от дебаг-версии

### 1. Использование WSGI-сервера (Gunicorn вместо `flask run`)

- **В дебаге:** Встроенный сервер Werkzeug однопоточный, медленный и не рассчитан на нагрузки.
- **В проде:** Запускается **Gunicorn**. Параметр `--workers 4` поднимет 4 отдельных процесса Python, обработка запросов станет параллельной и отказоустойчивой (если один воркер упадёт, остальные продолжат работать).

> 💡 *Примечание:* Для работы этой команды `gunicorn` должен быть прописан в вашем `requirements.txt` и установлен в образ.

### 2. Никаких volumes с исходным кодом

- **В дебаге:** Пробрасывался локальный код (`volumes: - .:/app`), чтобы править файлы на лету.
- **В проде:** Контейнер использует **только тот код, который вшит в Docker-образ при сборке**. Это гарантирует неизменяемость среды (Immutability).

### 3. Автоматический перезапуск (`restart: always`)

Если приложение упадет из-за критической ошибки или нехватки памяти, Docker сам перезапустит контейнер.

### 4. Проверка состояния (`healthcheck`)

Docker и внешние оркестраторы будут знать, действительно ли Flask отвечает на запросы, а не просто "висит" как процесс.

### 5. Ротация логов (`logging`)

Без настройки `max-size` логи Docker могут разрастись и забить всё дисковое пространство на сервере. Ротация ограничивает размер файлов логов.

---

### Как это правильно запускать на сервере?

Собираем образ и поднимаем прод-стек в фоновом режиме:

```bash
docker compose -f compose.prod.yaml up -d --build

```

`docker compose -f compose.prod.yaml up -d`

`docker compose -f compose.prod.yaml logs -f`

`docker run --rm -it learnpython:latest pip list`

`docker exec service2image-prod pip list`

### изменить политику перезапуска

#### прямо у работающего или остановленного контейнера через CLI Docker

`docker update --restart=no service2image-prod`

#### Изменить в compose

- restart: always - дает указание демону Docker (docker.service), который сам автозапускается вместе с ОС, автоматически поднимать этот контейнер после старта системы (и при любых падениях контейнера)

- restart: "no" — контейнер никогда не запускается автоматически (ни при падении, ни при перезагрузке ОС)

- restart: on-failure — перезапускается только если аварийно упал (с ненулевым кодом выхода), но при плановой перезагрузке ОС подниматься не будет

- restart: unless-stopped — будет автозапускаться при перезагрузке ОС только если ты вручную не остановил его командой docker compose down или docker stop перед перезагрузкой

#### Быстрая проверка политики

Посмотреть текущий режим restart для контейнера можно командой:

`docker inspect service2image-prod --format '{{ .HostConfig.RestartPolicy.Name }}'`
