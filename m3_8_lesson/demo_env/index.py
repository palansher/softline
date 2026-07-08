# set DB_HOST=localhost
# set DB_PORT=5433

import os

from dotenv import load_dotenv
load_dotenv()  # Загружает переменные из .env файла

db_host = os.environ.get('DB_HOST')  # Теперь из файла

print(db_host)
