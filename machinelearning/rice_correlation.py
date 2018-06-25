import pandas as pd
import numpy as np
from df_functions import load_production_data, get_data_selection, getLinkedProduct, \
    overlap_in_years, overlap_in_countries

def get_rice_related_products(df):
    products = [p.lower() for p in df._product.unique()]
    rice = [p.capitalize() for p in products if 'rice' in p]
    rice_related = get_data_selection(df, None, None, rice)
    return rice_related

def get_overlapping_data(df1, df2):
    products = df1._product.unique().tolist()
    linked_products = [getLinkedProduct(p) for p in products]
    year_overlap = overlap_in_years(df1, df2)
    country_overlap = overlap_in_countries(df1, df2)
    newdf1 = get_data_selection(df2, country_overlap, year_overlap, linked_products)
    newdf2 = get_data_selection(df1, country_overlap, year_overlap, products)
    return newdf1, newdf2

def year_price_correlation(food_df):



if __name__ == '__main__':
    food_df = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/onlycountry_year_average_data.csv')
    prod_df = load_production_data()
    rice_products = get_rice_related_products(food_df)
    food_rice, prod_rice = get_overlapping_data(food_df, prod_df)
