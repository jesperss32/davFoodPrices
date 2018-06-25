import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

df = pd.read_csv('reduced_production_data.csv', encoding='utf-8')

def unitCheck():
# check if unit is the same everywhere
    units = set(df['Unit'].tolist())
    print(units)
    # it is tonnes for every entry

def findNans(column):
    amountOfNaNs = 0
    zero_areas = []
    nan_areas = []
    zeros = 0
    for _, row in df.iterrows():
        if row[column] == 0:
            zeros +=1
            zero_areas.append(row['Area'])
        elif np.isnan(row[column]):
            amountOfNaNs += 1
            nan_areas.append(row['Area'])

    print("There are {} rows with NaNs and {} rows with zeros".format(amountOfNaNs, zeros))
    print("The countries with zeros in them are {}".format(sorted(list(set(zero_areas)))))
    print("The countries with NaNs in them are {}".format(sorted(list(set(nan_areas)))))

def removeNans(df):
    cleaned_df = df.dropna(subset=['Value'])
    return cleaned_df

removeNans(df).to_csv('cleaned_reduced_production.csv')
