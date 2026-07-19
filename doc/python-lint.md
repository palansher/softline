# Поверка синтаксиса и линтеры для Python кода

## compiler check

```bash
$ /home/vp/code/learn-python/.venv/bin/python -m py_compile /home/vp/code/learn-python/m3_2hw/app.py /home/vp/code/learn-python/m3_2hw/connect_db.py /home/vp/code/learn-python/m3_2hw/routes/*.py

# (no output)
```

## pyright linter

в .venv проекта:

```
pip install pyright
```

Запустить pyright можно в текущем каталоге, так и с отдельными файлами.
