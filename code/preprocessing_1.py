import pandas as pd
import numpy as np

from datetime import datetime as dt


df_original = pd.read_csv('data/raw/vendas-por-fatura.csv')
df = df_original.copy()

print(df.head())
print(df.info())

df.columns = ['id_transaction', 'date', 'id_client', 'country', 'products', 'monetary']


df_idNull = df[df['id_client'].isna()].reset_index(drop=True)
df_idNull = df_idNull.fillna('Unknown')


df = df.dropna()
df['id_client'] = df['id_client'].apply(lambda x: str(int(x))) # client id to string
df = pd.concat([df, df_idNull], axis=0).reset_index(drop=True)

df['date'] = df['date'].apply(lambda x: dt.strptime(x, '%m/%d/%Y')) # date to datetime
df['date'] = df['date'].apply(lambda x: x.format('%Y-%m-%d %H:%M:%S'))
df['monetary'] = df['monetary'].apply(lambda x: float(x.replace(',', '.'))) # replacing ',' for '.' and converting to float


df = df.drop_duplicates(keep='first')
df = df[~(df['monetary'] < 0)].reset_index(drop=True)

df.to_csv('data/processed/preProcessed.csv', index=False, date_format='iso')