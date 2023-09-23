import pandas as pd
import numpy as np
import sqlite3
#import roman
#from datetime import datetime
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
# kategorikus: REGION Előfizető lakóhelyének állama
# Dátum: TECHNICAL_COMMENCEMENT_DATE Előfizetés kezdetének technikai dátuma
# Diszkrét számértékű: PRODUCT Termékkód
# Folytonos számértékű: WEEKLY_FEE Előfizetés heti díja dollárban

# 2.1 b)
df_subs['TECHNICAL_COMMENCEMENT_DATE'].min() # 2016 02 01
df_subs['TECHNICAL_COMMENCEMENT_DATE'].max() # 2020 03 01
df_subs_groupby_TECHNICAL_COMMENCEMENT_DATE = df_subs.groupby("TECHNICAL_COMMENCEMENT_DATE").agg(
        Elemszam = ("TECHNICAL_COMMENCEMENT_DATE", "count"),
)

df_subs_groupby_PRODUCT = df_subs.groupby("PRODUCT").agg(
        Elemszam = ("PRODUCT", "count"),
)

df_subs['WEEKLY_FEE'].max() # 5.3
df_subs['WEEKLY_FEE'].min() # 0.0022
df_subs['WEEKLY_FEE'].hist()

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

#df_clients['BIRTH_DATE_MONTH'] = df_clients['BIRTH_DATE'].apply(lambda x: convert_roman_month_to_normal(x))
#def convert_roman_month_to_normal(input_date):
#   if(":" in input_date):
#       return int(input_date[5:7])
#   month_roman  = input_date.split("-")[1].strip().replace(('.'), '')
#   month_normal = roman.fromRoman(month_roman)
#    return int(month_normal)


# 2.3
df_subs['ONLINE_STATUS'].value_counts()

df_subs['ONLINE_STATUS_FORMATTED'] = df_subs["ONLINE_STATUS"].apply(lambda x: formatStatus(x))


def formatStatus(status):
    if status == "In-Person" or status == "Face2Face":
        return "Offline"
    if status == "On Web":
        return "Online"
    if status == "Digit sign." or status == "IN-Person digit signed" or status == "With Digital Cerificate":
        return "Offline - Digital signature"
    return status





