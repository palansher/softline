from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# conda install sqlalchemy psycopg2

# Получаем путь к папке, где лежит текущий скрипт
script_dir = Path(__file__).parent

# engine = create_engine('postgresql://postgres:postgres@localhost:5433/june02')
engine = create_engine('postgresql://postgres:admin@localhost/shop_db_hw3_2')

query = 'SELECT * from v_catalog_display'

df = pd.read_sql(query,engine)

df.to_excel(script_dir / "cars2.xlsx",index=False,sheet_name="Автомобили")
print(df)
