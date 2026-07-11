# Используем официальный образ Python в качестве базового
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем текущий каталог в контейнер
COPY . /app

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Делаем порт 5000 доступным для внешнего мира
EXPOSE 5000

# Определяем переменную окружения
ENV NAME World

# Запускаем приложение Flask
CMD ["python", "app.py"]
