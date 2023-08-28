import pandas as pd
import numpy as np

data = pd.read_csv('data/processed/df_rfm.csv')
df = data.copy()

df.tail()

df['R_rank'] = df['recency'].rank(ascending=False)
df['F_rank'] = df['frequency'].rank(ascending=True)
df['M_rank'] = df['monetary'].rank(ascending=True)
 
# We will normalize the data using rank normalization
# So we rank all the customers based on each of requisites for RFM and divide for the max rank 
df['R_rank_norm'] = (df['R_rank']/df['R_rank'].max())*100
df['F_rank_norm'] = (df['F_rank']/df['F_rank'].max())*100
df['M_rank_norm'] = (df['M_rank']/df['M_rank'].max())*100

# We need to weight the 3 attributes of RFM to make it all 100%. So we're using close weights of a text i've found in my research:
# 15% recency, 30% frquency, 55% monetary

df['RFM_Score'] = 0.15*df['R_rank_norm']+ 0.30*df['F_rank_norm']+0.55*df['M_rank_norm']
df['RFM_Score'] *= 0.05
df = df.round(2)
df[['id_client', 'RFM_Score']].head()


#Based on my research too, we set this classification for the clients based on their RFM score
df["segment"] = np.where(df['RFM_Score'] > 4.5, "Top",
                        (np.where(df['RFM_Score'] > 4,    'High value',
                        (np.where(df['RFM_Score'] > 3,    'Medium Value',
                         np.where(df['RFM_Score'] > 1.6,  'Low Value', 
                                                              'Lost Customers'))))))
df['segment'].value_counts()


top_high = df[(df['segment'] == 'Top') | (df['segment'] == 'High value')]
print(round(len(top_high)/len(df) * 100, 2), '% of customers were cassificated as Top or High Value')
print(round(top_high['monetary'].sum() / df['monetary'].sum() * 100, 2), '% of total earnings come from Top and High Value costumers')

lost = df[(df['segment'] == 'Lost Customers')]
print(round(len(lost)/len(df) * 100, 2), '% of customers were cassificated as Lost Customers')