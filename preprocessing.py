import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator


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
'Exchange rate (unofficial)', 'Electricity', 'Cotton']

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
    while thres <= len(prod_data.year.unique().tolist()):
        tempdf = delete_years_below_thres(prod_data, thres)
        countries = tempdf.country.unique().tolist()

        overlapping = tempdf.year.unique().tolist()
        for country in countries:
            country_data = tempdf.loc[df['country'] == country]
            years_available = country_data.year.unique().tolist()
            overlap = [y for y in years_available if y in overlapping]
            overlapping = overlap
        ys.append(len(overlapping))
        cs.append(len(countries))
        # if len(countries) > best_countries_count:
        #     best_countries_count = len(countries)
        #     best_countries = countries
        # if len(year) > best_years_count:
        #     best_years_count = len(year)
        #     best_years = year
        thres += 1
    l1, = plt.plot(range(len(prod_data.year.unique().tolist())+1),cs, label='countries')
    l2, =plt.plot(range(len(prod_data.year.unique().tolist())+1),ys, label='years_available')
    plt.legend(handles=[l1, l2])
    plt.show()

# find_country_year_entries(food_df_fo, 'Maize')
#print(food_df_fo.unit.unique().tolist())


def unit_normalization(df):
    products = df._product.unique().tolist()
    for product in products:
        pr_dt = df.loc[df['_product']== product]
        units = pr_dt.unit.unique().tolist()
        if len(units) > 1:
            print(product, units)
            for unit in units:
                unit_ind = pr_dt.loc[pr_dt['unit'] == unit].index.values
                if 'KG' in unit:
                    if unit == 'KG':
                        continue
                    measure = unit.replace('KG', '').replace(' ', '')
                    measure = float(measure)

                    df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
                    df.loc[unit_ind, 'unit'] = 'KG'
                elif 'MT' in unit:
                    measure = 1000
                    df.loc[unit_ind, 'price'] = df.loc[unit_ind, 'price'] / measure
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
                elif 'Head' in unit:
                    df.loc[unit_ind, 'unit'] = 'Unit'
                elif 'Loaf' in unit:
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

    return df
newdf = unit_normalization(food_df_fo)
print('\n\n\n')
unit_normalization(newdf)
