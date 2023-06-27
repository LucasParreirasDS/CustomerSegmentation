import pandas as pd
import numpy as np

from datetime import datetime as dt


df_original = pd.read_csv('data/processed/preProcessed.csv', parse_dates=['date'])
df = df_original.copy()


# Sorting the data by client id and date
data_date = df[['id_client', 'date']].sort_values(['id_client', 'date']).reset_index(drop=True)  
data_date.head(10)



count = 1 # starting the count
client_date = {} # creating a dict to store client data about dates
first_day = data_date['date'][0]
last_day = data_date['date'][0]
for idx, row in data_date.iterrows():
  if idx != len(data_date)-1:
    if row['id_client'] == data_date['id_client'][idx+1]:
      count += 1                                                       # (How many transactions in this time?)
      last_day = data_date['date'][idx+1]                              # (When was the last?)
    else:
      client_date[row['id_client']] = [first_day, last_day, count]
      count = 1
      first_day = data_date['date'][idx+1]                             # (When was the first transaction for each customer?)
      last_day = data_date['date'][idx+1]
  else:
      client_date[row['id_client']] = [first_day, last_day, count]
      

# Creating the dataframe for informations about date
df_client = pd.DataFrame(client_date).T
df_client.reset_index(inplace=True)
df_client.columns = ['id_client', 'first_day', 'last_day', 'frequency']

# How many days is the customer a member? It will be used for normalize data
interval = df_client['last_day']- df_client['first_day']
interval = interval.apply(lambda x: x.days)


df_client['interval'] = interval
df_client['frequency'] = pd.to_numeric(df_client['frequency'])
df.head()

# We will calculate de Recency (from RFM) that is the last day the costumer made an action. 
  ## We need a number of days to actual date. I'm coding this in 05/2022 (reviewing in 06/2023), and the last transaction of data set was beginning of December 2021, so i will consider the actual date as December 31 2021.
  
recency = []
date = dt.strptime('2021-12-31', '%Y-%m-%d')
df_client['last_day'].apply(lambda x: recency.append(date-x))

recency_days = []
for c in range(len(df_client)):
    recency_days.append(int(str(recency[c]).split()[0])) # splitting to get only the number of days
    
df_client['recency'] = recency_days

# Selecting columns to merge and create our dataframe to be used
data_clients = df.groupby('id_client').sum(numeric_only=True).sort_values('monetary', ascending=False).reset_index()


# Creating dataframe with RFM information
df_rfm = df_client.merge(data_clients[['id_client', 'monetary']], on='id_client').sort_values('monetary', ascending=False).reset_index(drop=True)
df_rfm.head()

df_rfm.to_csv('data/processed/df_rfm.csv', index=False)