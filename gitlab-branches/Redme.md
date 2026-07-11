После создания этих файлов, вы можете собрать Docker-образ и запустить контейнер с помощью следующих команд:

```shell
docker build -t task1-flask-app .
docker run -p 5000:5000 task1-flask-app
```

Теперь вы сможете получить список веток, выполнив запрос к `http://localhost:5000/branches`.
