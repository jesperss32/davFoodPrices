import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator
import copy

def load_food_data():
    ''' Loads foodprices table and renames its columns'''
    df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')
    df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
                       'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
                       'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
                       'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
                       'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
                       'mp_commoditysource' : 'source'}, inplace=True)
    return df


def delete_products(df, to_delete):
    df = df[~df['_product'].isin(to_delete)]
    return df

food_df = load_food_data()

nonfoods = ['Fuel (diesel)', 'Fuel (petrol-gasoline)', 'Fuel (kerosene)', 'Fuel (gas)', \
'Charcoal', 'Exchange rate', 'Wage (non-qualified labour, non-agricultural)', \
'Wage (non-qualified labour)', 'Wage (qualified labour)', 'Wage (non-qualified labour, agricultural)', \
'Exchange rate (unofficial)', 'Electricity', 'Cotton', 'Transport (public)']

food_df_fo = delete_products(food_df, nonfoods)



def unit_normalization(df):
    units = df.unit.unique().tolist()
    for unit in units:
        unit_ind = df.loc[df['unit'] == unit].index.values
        if 'KG' in unit:
            if unit == 'KG':
                continue
            measure = unit.replace('KG', '').replace(' ', '')
            measure = float(measure)
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
            df.loc[unit_ind, 'unit'] = 'KG'
        elif 'MT' in unit:
            measure = 1000
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price']/measure
            df.loc[unit_ind, 'unit'] = 'KG'

        elif 'Gallon' in unit:
            measure = 3.78541178
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
            df.loc[unit_ind, 'unit'] = 'L'
        elif 'Pound' in unit:
            measure = 0.45359237
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] * measure
            df.loc[unit_ind, 'unit'] = 'KG'
        elif 'Libra' in unit:
            measure = 1 / 0.329
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] * measure
            df.loc[unit_ind, 'unit'] = 'KG'
        elif 'Cuartilla' in unit:
            measure = 2.875575 ##?????
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
            df.loc[unit_ind, 'unit'] = 'KG'
        elif 'pcs' in unit:
            if unit == 'pcs':
                df.loc[unit_ind, 'unit'] = 'Unit'
                continue
            measure = float(unit.replace(' pcs', ''))
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
            df.loc[unit_ind, 'unit'] = 'Unit'
        elif 'Dozen' in unit:
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / 12
            df.loc[unit_ind, 'unit'] = 'Unit'
        elif 'Head' in unit or 'Loaf' in unit or 'Packet' in unit:
            df.loc[unit_ind, 'unit'] = 'Unit'
        elif ' G' in unit:
            if unit == 'G':
                continue
            measure = unit.replace('G', '')
            measure = float(measure)
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] *(1000 / measure)
            df.loc[unit_ind, 'unit'] = 'KG'
        elif 'ML' in unit:
            if unit == 'ML':
                continue
            measure = unit.replace('ML', '').replace(' ', '')
            measure = float(measure)
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] *(1000 / measure)
            df.loc[unit_ind, 'unit'] = 'L'
        elif ' L' in unit:
            if unit == 'L':
                continue
            measure = unit.replace(' L', '')
            measure = float(measure)
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
            df.loc[unit_ind, 'unit'] = 'L'
        elif 'Cubic meter' in unit:
            df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] * 1000
            df.loc[unit_ind, 'unit'] = 'L'
    return copy.deepcopy(df)

food_df_un = unit_normalization(food_df_fo)

# print(food_df_un.unit.unique().tolist())
# food_df_un.to_csv('firstclean_foodprices_data.csv')
