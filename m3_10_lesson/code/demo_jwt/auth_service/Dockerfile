FROM python:latest
#Установка рабочей директории внутри контейнера
WORKDIR /app

#Копирование файла зависимостей в контейнер
COPY requirements.txt .

#Установка зависимостей
#--no-cache-dir - для уменьшения размера образа
RUN pip install --no-cache-dir -r requirements.txt

COPY .  .

EXPOSE 5001

ENV FLASK_ENV=production

CMD ["gunicorn","--bind","0.0.0.0:5001","app:app"]