import docker

# from_env - читаем переменные окружения Docker(DOCKER_HOST...)
client = docker.from_env()

# Останавливаем и удаляем контейнеры с postgres и adminer

containers = ['postgres-db','adminer-ui']

for title_container in containers:
    try:
        exist_container = client.containers.get(title_container)
        exist_container.stop() #аналог команды docker stop
        exist_container.remove() #аналог команды docker rm
        print('Удален старый контейнер',title_container)
    except docker.errors.NotFound:
        print('Процесс удаления контейнера пропущен, т.к. контейнер не найден')

# Скачаем образы и запустим на их основе контейнеры

client.containers.run(
    'postgres:15-alpine', #имя  образа
    name='postgres-db', #имя контейнера
    environment={'USER':'postgres', 'PASSWORD':'123'},
    ports={'5435/tcp':5435},
    detach=True, #запуск в фоновом режиме

)

print('Postgres запущен на порту 5435')

# Установка adminer

client.containers.run(
    'adminer:latest',
    name='adminer-ui',
    ports={'8080/tcp':8080},
    detach=True
)

client.containers.run(
    'python:3.15.0a6-slim-trixie', #имя  образа
    name='python', #имя контейнера
    detach=True, #запуск в фоновом режиме

)

started_containers = client.containers.list()
for container in started_containers:
    print(container.name)
    print(container.status)
    print("Adminer: http://127.0.0.1:8080")

# Практика - скачать образ python и запустить контейнер