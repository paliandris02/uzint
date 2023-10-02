"""
VBII48 Páli András
"""

import pandas as pd
import numpy as np
import sqlite3
import math

conn = sqlite3.connect('magazine_subscriptions.db')
c = conn.cursor()
c.execute('select * from sqlite_master WHERE type ="table";')
tables = c.fetchall()
tables


df_subs = pd.read_sql_query('select * from Subscriptions', conn)
df_subs.info()

# 2.5

rewardProgram = pd.read_excel('RewardProgram.xlsx')

rwDuplicatesBool = rewardProgram.duplicated()
rwDuplicates = pd.DataFrame()

for i, row in enumerate(rwDuplicatesBool,start=0):
    if row:
        rwDuplicates = rwDuplicates.append(rewardProgram.iloc[i])

rwDuplicates
rwDuplicates['AGENCY'].value_counts()

rwCleaned = rewardProgram.drop_duplicates()

merged_subs= pd.merge(df_subs,rwCleaned, on='SubscriptionID', how='left')
merged_subs = merged_subs.fillna('Nincs')

# 2.6
df_subs_not_online = pd.DataFrame()

def formatStatus(status):
    if status == "In-Person" or status == "Face2Face":
        return "Offline"
    if status == "On Web":
        return "Online"
    if status == "Digit sign." or status == "IN-Person digit signed" or status == "With Digital Cerificate":
        return "Offline - Digital signature"
    return status

df_subs['ONLINE_STATUS_FORMATTED'] = df_subs["ONLINE_STATUS"].apply(lambda x: formatStatus(x))

for i,row in df_subs.iterrows():
    if row['ONLINE_STATUS_FORMATTED'] != 'Online':
        df_subs_not_online = df_subs_not_online.append(row)

df_subs_not_online = df_subs_not_online[(df_subs_not_online['REGION'] == 'TX') | 
                                        (df_subs_not_online['REGION'] == 'MA') | 
                                        (df_subs_not_online['REGION'] == 'SC') |
                                        (df_subs_not_online['REGION'] == 'UT') | 
                                        (df_subs_not_online['REGION'] == 'LA') 
                                        ]

df_subs_not_online.groupby('REGION').agg(
        Heti_elofizetes = ('REGION', 'count'),
        Dijbevetel = ('WEEKLY_FEE', 'sum')
)

df_subs_not_online.reset_index(inplace=True)

# anomália javítás - valószínű, hogy UT, TX rekordoknál a tizedesvessző kettővel elcsúszott 
df_subs_not_online["WEEKLY_FEE_JAVITOTT"]=''
for i in range(len(df_subs_not_online)):
    if df_subs_not_online["REGION"][i] in ("TX", "UT"):
        df_subs_not_online["WEEKLY_FEE_JAVITOTT"][i]=float(df_subs_not_online["WEEKLY_FEE"][i])*100
    else:
        df_subs_not_online["WEEKLY_FEE_JAVITOTT"][i]=df_subs_not_online["WEEKLY_FEE"][i]

df_subs_not_online.groupby('REGION').agg(
        Heti_elofizetes = ('REGION', 'count'),
        Dijbevetel = ('WEEKLY_FEE_JAVITOTT', 'sum')
)

kvartilisek = df_subs_not_online['WEEKLY_FEE_JAVITOTT'].quantile([0.25, 0.5, 0.75])

df_subs_not_online["RATING"]=''
for i in range(len(df_subs_not_online)):
    if df_subs_not_online["WEEKLY_FEE_JAVITOTT"][i]<kvartilisek[0.25]:
        df_subs_not_online["RATING"][i]="Weak"
    elif df_subs_not_online["WEEKLY_FEE_JAVITOTT"][i]<kvartilisek[0.75]:
        df_subs_not_online["RATING"][i]="Moderate"
    else:
        df_subs_not_online["RATING"][i]="Strong"
        
        
# 2.7

df_ChurnCodes = pd.read_sql_query('select * from ChurnCodes', conn)

df_subs['Churn_Status'] = ''
for i in range(len(df_subs)):
    if df_subs['STATUS_REASON'][i] == 'retrmnt' or df_subs['STATUS_REASON'][i] == 'invldty' or df_subs['STATUS_REASON'][i] == 'deseased':
        df_subs['Churn_Status'][i] = 0
    else:
        df_subs['Churn_Status'][i] = 1

# 2.8
df_subs['Months_Since_Commencement'] = ''

for i in range(len(df_subs)):
    if df_subs['Churn_Status'][i] == 0:
         temp = pd.to_datetime('2020-03-01') - pd.to_datetime(df_subs['TECHNICAL_COMMENCEMENT_DATE'][i])
         df_subs['Months_Since_Commencement'][i] = math.floor(int(str(temp).split(' ')[0])/30)
    else:
         temp = pd.to_datetime(df_subs['VERSION_START_DATE'][i]) - pd.to_datetime(df_subs['TECHNICAL_COMMENCEMENT_DATE'][i])
         if(math.floor(int(str(temp).split(' ')[0])/30) < 1):
             df_subs['Months_Since_Commencement'][i] = 1
         else:             
            df_subs['Months_Since_Commencement'][i] =  math.floor(int(str(temp).split(' ')[0])/30)
         







