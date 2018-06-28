import pandas as pd
import numpy as np
from df_functions import load_production_data, get_data_selection, getLinkedProduct, \
    overlap_in_years, overlap_in_countries
from scipy.stats import spearmanr

def get_overlapping_data(df1, df2):
    products = df1._product.unique().tolist()
    linked_products = [getLinkedProduct(p) for p in products]
    year_overlap = overlap_in_years(df1, df2)
    country_overlap = overlap_in_countries(df1, df2)
    newdf1 = get_data_selection(df2, country_overlap, year_overlap, linked_products)
    newdf2 = get_data_selection(df1, country_overlap, year_overlap, products)
    return newdf1, newdf2

def product_correlation(food_df):
    products = food_df._product.unique().tolist()
    for p in range(1, len(products)):
        product_data1 = get_data_selection(food_df,None, None, [products[p]])
        product_data2 = get_data_selection(food_df,None, None, [products[p-1]])
        if len(product_data1) == len(product_data2):

            corr = spearmanr(product_data1['price'], product_data2['price'])
            rho, pval = corr
            print(rho, pval)
            print(products[p], products[p-1])




if __name__ == '__main__':
    food_df = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/onlycountry_year_average_data.csv')
    prod_df = load_production_data()
    food_rice, prod_rice = get_overlapping_data(food_df, prod_df)
    product_correlation(get_data_selection(food_df, ['India'], None, None))
