"""
VBII48 Páli András
"""

import pandas as pd
import numpy as np
import sqlite3
import roman
from datetime import datetime
#import matplotlib.pyplot as plt


conn = sqlite3.connect('magazine_subscriptions.db')
c = conn.cursor()
c.execute('select * from sqlite_master WHERE type ="table";')
tables = c.fetchall()
tables


df_subs = pd.read_sql_query('select * from Subscriptions', conn)
df_subs.info()


# 2.1 a)
df_subs['WEEKLY_FEE'].value_counts()
df_subs['PRODUCT'].value_counts()
# kategorikus: STATUS_PORTFOLIO, STATUS_REASON, PRODUCT_TYPE, AGENCY, REGION, CITY, ONLINE_STATUS
# Dátum: TECHNICAL_COMMENCEMENT_DATE, VERSION_START_DATE
# Diszkrét számértékű: PRODUCT, SubsID, ClientID
# Folytonos számértékű: WEEKLY_FEE

# 2.1 b)
df_subs['TECHNICAL_COMMENCEMENT_DATE'].min() # 2016 02 01
df_subs['TECHNICAL_COMMENCEMENT_DATE'].max() # 2020 03 01
df_subs_groupby_TECHNICAL_COMMENCEMENT_DATE = df_subs.groupby("TECHNICAL_COMMENCEMENT_DATE").agg(
        Elemszam = ("TECHNICAL_COMMENCEMENT_DATE", "count"),
)

df_subs['PRODUCT'].max() # 13409
df_subs['PRODUCT'].min() # 13226

df_subs_groupby_PRODUCT = df_subs.groupby("PRODUCT").agg(
        Elemszam = ("PRODUCT", "count"),
)

df_subs['WEEKLY_FEE'].max() # 5.3
df_subs['WEEKLY_FEE'].min() # 0.0022
df_subs['WEEKLY_FEE'].hist(bins=50)

df_clients = pd.read_sql_query('select * from Clients', conn)
df_clients.info()
df_clients.describe(include="all")
df_clients.groupby(['BIRTH_DATE'])['ClientID'].count()


df_clients['BIRTH_DATE_YEAR'] = [i[0:4] if i[0:4].isnumeric() ==True else '19'+i[-2:] for i in df_clients['BIRTH_DATE']]
df_clients['BIRTH_DATE_YEAR'].max() # 2002 18
df_clients['BIRTH_DATE_YEAR'].min() # 1906 114

df_clients['BIRTH_DATE_YEAR'].hist(bins=8) # ebből sok minden nem látszik

# gyakorisági tábla
gyaktábla = np.histogram(df_clients['BIRTH_DATE_YEAR'].astype(int), bins=10)
gyaktábla = pd.DataFrame(gyaktábla).transpose()
gyaktábla.columns =(['Gyakoriság', 'Alsó határ'])
gyaktábla['Felső határ'] = gyaktábla['Alsó határ'].shift(-1)
gyaktábla = gyaktábla[['Alsó határ','Felső határ', 'Gyakoriság']]
gyaktábla = gyaktábla.drop(10, axis = 'index')


# 2.2
df_clients['BIRTH_DATE_YEAR']

df_clients['BIRTH_DATE_MONTH'] = df_clients['BIRTH_DATE'].apply(lambda x: convert_roman_month_to_normal(x))

df_clients['BIRTH_DATE_DAY'] = df_clients['BIRTH_DATE'].apply(lambda x: extractDayFromDate(x))

df_clients['BIRTH_DATE_FORMATTED'] = df_clients['BIRTH_DATE_YEAR'].astype(str) +'-'+ df_clients['BIRTH_DATE_MONTH'].astype(str) + '-' + df_clients['BIRTH_DATE_DAY'].astype(str)

df_clients['BIRTH_DATE_FORMATTED'] = df_clients['BIRTH_DATE_FORMATTED'].apply(lambda x: formatToDateTime(x))

df_clients['AGE'] = (pd.to_datetime('2020-03-01')- df_clients['BIRTH_DATE_FORMATTED'])/365.25

def formatToDateTime(date):    
    return pd.to_datetime(date)

def extractDayFromDate(date):
    if ":" in date:
        if len(date) == 1:
            return '0' + date[8:9]
        else:
            return date[8:10]
    if len(date.split("-")[0].strip()) == 1:
        return '0' + date.split("-")[0].strip()
    else:
        return date.split("-")[0].strip()

def convert_roman_month_to_normal(input_date):
   if(":" in input_date):
       if len(input_date[5:7]) == 1:
           return '0' + str(input_date[5:7])
       else: 
           return str(input_date[5:7])
   month_roman  = input_date.split("-")[1].strip().replace(('.'), '')
   month_normal = roman.fromRoman(month_roman)
   if len(str(month_normal)) == 1:
       return '0' + str(month_normal)
   else: 
       return str(month_normal)


# 2.3
df_subs['ONLINE_STATUS'].value_counts()

df_subs['ONLINE_STATUS_FORMATTED'] = df_subs["ONLINE_STATUS"].apply(lambda x: formatStatus(x))

df_subs['ONLINE_STATUS_FORMATTED'].value_counts()

def formatStatus(status):
    if status == "In-Person" or status == "Face2Face":
        return "Offline"
    if status == "On Web":
        return "Online"
    if status == "Digit sign." or status == "IN-Person digit signed" or status == "With Digital Cerificate":
        return "Offline - Digital signature"
    return status





