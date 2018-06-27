import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from df_functions import load_percentage_product_data, get_data_selection, regions,\
    getLinkedProduct, overlap_in_years, overlap_in_countries, getPriceLinkedProduct
from operator import itemgetter
from prod_price_cor_regions import get_overlapping_data, year_average, \
    align_years, correlation, year_country_average

def month_price_correlation(df):
    years = df.year.unique().tolist()
    for prod in df._product.unique().tolist():
        product_data = get_data_selection(df, None, None, [prod])
        for year in years:
            year_data = get_data_selection(df, None, [year], None)
            months = year_data['month']
            price_changes = year_data['price_change']
            corr, pval = spearmanr(months, price_changes)
            if pval <= 0.05 and corr > 0.5:
                print(prod, year, corr)



if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/only_complete_years_data_percentages.csv')
    month_price_correlation(food_data)
