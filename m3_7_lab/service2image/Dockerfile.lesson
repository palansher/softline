FROM python:3.13-alpine3.19

# Переносим файл requirements.txt из проекта в образ докер
COPY requirements.txt /app/requirements.txt

# Переходим в папку образа
WORKDIR /app

# Устанавливаем все зависимости в эту папку
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5005

CMD ["python", "app.py"]

#Для создания образа используйте команду
#docker build -t flask-app .
#1) docker build : это команда для сборки докер образа на основе докер файла
#2) -t flask-app : задаем имя образа
#3) . это где искать докер файл
