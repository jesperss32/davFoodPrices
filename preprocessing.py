import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## DATA LOAD FUNCTIONS ########################################################
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

def load_production_data():
    '''Loads production table and renames its columns'''
    production_df = pd.read_csv('reduced_production_data.csv', encoding='latin-1')
    production_df.rename(columns={'Area' : 'country', 'Item' : '_product', 'Year' : 'year', \
                        'Unit' : 'unit', 'Value' : 'value'}, inplace=True)
    return production_df


food_df = load_food_data()
prod_df = load_production_data()

## MATPLOTLIB TEST ####################
def visualize_year_availability():
    ''' Makes a bar plot of the data availability of products in all countries
        for each year'''
    years = food_df.year.unique().tolist()
    year_freqs = {}
    for year in years:
        year_freqs[year] = 0

    for _, entry in food_df.iterrows():
        key = entry['year']
        year_freqs[key] += 1

    plt.bar(year_freqs.keys(), year_freqs.values())
    plt.xlabel('Year')
    plt.ylabel('Data available')
    plt.show()

## table information extraction ########################
def list_years(df):
    years = np.sort(df.year.unique())
    return years

def list_countries(df):
    countries = df.country.unique()
    return countries

########### Data cleaning ####################################################

nonfoods = ['Fuel (diesel)', 'Fuel (petrol-gasoline)', 'Charcoal', 'Exchange rate', 'Wage (non-qualified labour, non-agricultural)', \
'Wage (non-qualified labour)', 'Wage (qualified labour)', 'Wage (non-qualified labour, agricultural)', \
'Exchange rate (unofficial)', 'Electricity', 'Cotton']

def delete_products(df, to_delete):
    df = df[~df['_product'].isin(to_delete)]
    return df

def product_entry_freq(df):
    products = df._product.unique().tolist()
    for product in products:
        product_data = df.loc[df['_product'] == product]
        entries = len(product_data)
        countries = len(product_data.country.unique().tolist())
        years = len(product_data.year.unique().tolist())
        months = len(product_data.month.unique().tolist())
        print('Product:', product)
        print('Entries:', entries, '\n Countries:', countries, '\n Years:', years, '\n Months:', months)

product_entry_freq(delete_products(food_df, nonfoods))
