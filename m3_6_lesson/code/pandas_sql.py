import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5433/june02')

query = 'SELECT title_mark,title_model FROM mark m1 INNER JOIN model m2 ON m1.mark_id=m2.mark_id'

df = pd.read_sql(query,engine)

df.to_excel("cars2.xlsx",index=False,sheet_name="Автомобили")
print(df)