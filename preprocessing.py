import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator
import copy
import matplotlib.ticker as ticker


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

nonfoods = ['Fuel (diesel)', 'Fuel (petrol-gasoline)', 'Fuel (kerosene)', 'Fuel (gas)', \
'Charcoal', 'Exchange rate', 'Wage (non-qualified labour, non-agricultural)', \
'Wage (non-qualified labour)', 'Wage (qualified labour)', 'Wage (non-qualified labour, agricultural)', \
'Exchange rate (unofficial)', 'Electricity', 'Cotton', 'Transport (public)']

def delete_products(df, to_delete):
    df = df[~df['_product'].isin(to_delete)]
    return df

food_df_fo = delete_products(food_df, nonfoods)

def product_entry_freq(df):
    products = df._product.unique().tolist()
    pef = {}
    for product in products:
        product_data = df.loc[df['_product'] == product]
        entries = len(product_data)
        countries = len(product_data.country.unique().tolist())
        years = len(product_data.year.unique().tolist())
        months = len(product_data.month.unique().tolist())
        pef[product] = (entries, countries, years, months)
    return pef

#pef = product_entry_freq(delete_products(food_df, nonfoods))
# for k, v in sorted(pef.items(), key=operator.itemgetter(1), reverse=True):
#     print(k, v)

#### data selection analysis ##################################################
def delete_years_below_thres(df, thres):
    '''Function to delete entries from the dataframe df that span up data about less than the thresholded
       amount of years.'''
    countries = df.country.unique().tolist()
    for country in countries:
        country_data = df.loc[df['country'] == country]
        years = country_data.year.unique().tolist()
        if len(years) <= thres:
            df = df.drop(country_data.index.tolist())
    return df


def countries_yearoverlap(df, thres):
    '''Function that returns N countries that have overlapping year data. It deletes the countries for which
       less than thres data is available first.'''
    newdf = delete_years_below_thres(df, thres)
    overlapping = newdf.year.unique().tolist()
    countries = newdf.country.unique().tolist()
    for country in countries:
        country_data = newdf.loc[df['country'] == country]
        years_available = country_data.year.unique().tolist()
        overlap = [y for y in years_available if y in overlapping]
        overlapping = overlap

    return len(countries),sorted(overlap)

def find_country_year_entries(df, product):
    prod_data = df.loc[df['_product'] == product]
    thres = 0
    # best_years_count = 0
    # best_countries_count = 0
    # best_years = None
    # best_countries = None
    cs = []
    ys = []
    best_cs = len(prod_data.country.unique())
    best_ys = 0
    while thres <= len(prod_data.year.unique().tolist()):
        tempdf = delete_years_below_thres(prod_data, thres)
        countries = tempdf.country.unique().tolist()

        overlapping = tempdf.year.unique().tolist()
        for country in countries:
            country_data = tempdf.loc[df['country'] == country]
            years_available = country_data.year.unique().tolist()
            overlap = [y for y in years_available if y in overlapping]
            overlapping = overlap
        ys.append( len(overlapping))
        cs.append( len(countries))
        thres += 1
    fig, ax = plt.subplots(1,1)
    l1, = ax.plot(range(len(prod_data.year.unique().tolist())+1),cs, label='countries')
    l2, = ax.plot(range(len(prod_data.year.unique().tolist())+1),ys, label='years_available')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    plt.title(product)
    plt.xlabel('threshold')
    plt.ylabel('year/country frequency')
    plt.legend(handles=[l1, l2])
    plt.show()

for product in food_df_fo._product.unique().tolist():
    find_country_year_entries(food_df_fo, product)
#print(food_df_fo.unit.unique().tolist())
