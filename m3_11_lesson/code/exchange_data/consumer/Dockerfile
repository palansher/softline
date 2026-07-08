FROM python:3.13-alpine3.22

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5005

CMD ["python","app.py"]