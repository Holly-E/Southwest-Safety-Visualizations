# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 17:48:56 2020

@author: Erick
"""
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
#%%

#df = pd.read_excel('API_IS.AIR.PSGR_Top rows removed.xlsx')
df = pd.read_excel('API_IS.AIR.PSGR_DS2_en_excel_v2_713999.xls')
Fatalities = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')

cols = df.iloc[2]
df.drop(df.index[[0,2]], inplace = True)
df.columns = cols
#%%
Totals = df.drop(['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], axis = 1)
Totals = Totals.replace(np.nan, 0)
#%%
newcols = list(Totals.columns)
intcols = [int(x) for x in newcols]
Totals.columns = intcols
#%%
Totals = pd.DataFrame(Totals.sum())
Totals = Totals.drop(Totals.index[0:10])

#%%
Totals = Totals.loc[1970:2009]

#%%
Totals.columns = ['Total Passengers']
Totals.index.name = 'Year'

#%%
"""
Data['Time'] = Data['Time'].replace(np.nan, '00:00') 
Data['Time'] = Data['Time'].str.replace('c: ', '')
Data['Time'] = Data['Time'].str.replace('c:', '')
Data['Time'] = Data['Time'].str.replace('c', '')
Data['Time'] = Data['Time'].str.replace('12\'20', '12:20')
Data['Time'] = Data['Time'].str.replace('18.40', '18:40')
Data['Time'] = Data['Time'].str.replace('0943', '09:43')
Data['Time'] = Data['Time'].str.replace('22\'08', '22:08')
Data['Time'] = Data['Time'].str.replace('114:20', '00:00') #is it 11:20 or 14:20 or smth else? 

Data['Time'] = Data['Date'] + ' ' + Data['Time'] #joining two rows
def todate(x):
    return datetime.strptime(x, '%m/%d/%Y %H:%M')
Data['Time'] = Data['Time'].apply(todate) #convert to date type
print('Date ranges from ' + str(Data.Time.min()) + ' to ' + str(Data.Time.max()))

Data.Operator = Data.Operator.str.upper()
"""
#%%
#= Data.copy
#Fatalities.Time = Fatalities.Time.apply(str)
#%%
died_dict = {}
Fatalities = Fatalities.replace(np.nan, 0)
for ind, row in Fatalities.iterrows():
    current = row['Date'][-4:]
    if current not in died_dict.keys():
        died_dict[current] = [row['Aboard'], row['Fatalities']]
    else:
        died_dict[current][0] += row['Aboard']
        died_dict[current][1] += row['Fatalities']
#del Fatalities['Time']

#%%
aboard_crashes = []
died = []
for ind, row in Totals.iterrows():
    aboard_crashes.append(died_dict[str(ind)][0])
    died.append(died_dict[str(ind)][1])

Totals['aboard crashes'] = aboard_crashes
Totals['Died'] = died
#%%
Totals['Ratio'] = Totals['Died'] / Totals['Total Passengers'] * 100 #calculating ratio

#%%
Totals.to_csv('years1970_2009.csv')