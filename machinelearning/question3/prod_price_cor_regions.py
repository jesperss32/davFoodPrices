import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from df_functions import load_percentage_product_data, get_data_selection, regions,\
    getLinkedProduct, overlap_in_years, overlap_in_countries, getPriceLinkedProduct
from operator import itemgetter
import os

def get_overlapping_data(proddf, fooddf):
    products = [p for p in fooddf._product.unique().tolist() if getLinkedProduct(p)]
    linked_products = [getLinkedProduct(p) for p in products if getLinkedProduct(p)]
    linked_products = [item for sublist in linked_products for item in sublist]
    year_overlap = overlap_in_years(fooddf, proddf)
    country_overlap = overlap_in_countries(fooddf, proddf)
    newdf1 = get_data_selection(proddf, country_overlap, year_overlap, linked_products)
    newdf2 = get_data_selection(fooddf, country_overlap, year_overlap, products)
    return newdf1, newdf2

def year_country_average(fooddf, column):
    new_fooddf = pd.DataFrame(columns=fooddf.columns.values)
    countries = fooddf.country.unique().tolist()
    years = fooddf.year.unique().tolist()
    for country in countries:
        for year in years:
            year_data = get_data_selection(fooddf, [country], [year], None)
            if year_data.empty:
                continue
            row = year_data.iloc[0]
            mean_pricechange = year_data[column].mean()
            row[column] = mean_pricechange
            new_fooddf = new_fooddf.append(row)
    return new_fooddf

def year_average(fooddf, column):
    new_fooddf = pd.DataFrame(columns=fooddf.columns.values)
    years = fooddf.year.unique().tolist()

    for year in years:
        year_data = get_data_selection(fooddf, None, [year], None)
        if year_data.empty:
            continue
        row = year_data.iloc[0]
        mean_pricechange = year_data[column].mean()
        row[column] = mean_pricechange
        new_fooddf = new_fooddf.append(row)
    return new_fooddf

def align_years(fooddf, proddf):
    newfood = pd.DataFrame(columns=fooddf.columns.values)
    newprod = pd.DataFrame(columns=proddf.columns.values)
    years = overlap_in_years(fooddf, proddf)
    countries = overlap_in_countries(fooddf, proddf)
    for country in countries:
        for year in years:
            food_entry = fooddf.loc[(fooddf['year']==year) & (fooddf['country'] == country)]
            prod_entry = proddf.loc[(proddf['year']==year) & (proddf['country'] == country)]
            # if len(food_entry) > len(prod_entry):
            #     food_entry = year_average(food_entry, 'price_change')
            # elif len(prod_entry) > len(food_entry):
            #     print(prod_entry)
            #     prod_entry = year_average(prod_entry, 'value_change')
            if food_entry.empty or prod_entry.empty:
                continue
            newfood = newfood.append(food_entry)
            newprod = newprod.append(prod_entry)
    return newfood, newprod

def correlation(prod_data, food_data):
    corr = spearmanr(prod_data['value_change'], food_data['price_change'])
    rho, pval = corr
    if pval <= 0.05:
        #
        # plt.scatter(prod_data['value_change'], food_data['price_change'])
        # plt.xlabel('production')
        # plt.ylabel('price')
        # plt.show()
        return corr
    return False


def region_correlation(region, r, food_data, prod_data):
    region_pricedata = get_data_selection(food_data, region)
    region_proddata = get_data_selection(prod_data, region)
    overlap_countries = overlap_in_countries(region_pricedata, region_proddata)
    region_price = get_data_selection(region_pricedata, overlap_countries)
    region_production = get_data_selection(region_proddata, overlap_countries)

    reg_production, reg_price = get_overlapping_data(region_production, region_price)

    region_priceprods = reg_price._product.unique().tolist()
    region_prodprods = reg_production._product.unique().tolist()

    for product in region_prodprods:
        linked = getPriceLinkedProduct(product)
        productprice = get_data_selection(reg_price, None, None, linked)

        productprod = get_data_selection(reg_production, None, None, [product])
        productprod, productprice = get_overlapping_data(productprod, productprice)

        productprice_averaged = year_country_average(productprice, 'price_change')
        productprod_averaged = year_country_average(productprod, 'value_change')

        newfood, newprod = align_years(productprice_averaged, productprod_averaged)
        corr = correlation(newprod, newfood)

        if corr:
            rho, pvalue=corr
            if (rho < -0.5 or rho > 0.5) and pvalue < 0.05 and rho != 1.0:
                print(r, '&', product, '&', round(rho,2) , '&', pvalue, '\\\\')
                print('\\hline')
                # cwd = os.getcwd()
                # os.chdir('/home/student/Documents/Projecten/davFoodPrices/machinelearning/question3/region_corr_improved')
                # df = pd.concat([newprod['value_change'], newfood['price_change']])
                # df.to_csv(r.replace(' ', '') + '_' + product.replace(' ', '') + 'correlation.csv')
                # os.chdir(cwd)
            # save_df = pd.concat([newprod['value_change'].reset_index(), newfood['price_change'].reset_index()], axis=1, ignore_index=True)
            # save_df.to_csv(r + '_'+product + '.csv')

if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/country_year_average_percentage_data.csv')
    prod_data = load_percentage_product_data()
    print(len(food_data), len(prod_data))
    europe, middle_east, asia, africa, south_america = regions()
    region_correlation(europe, 'europe', food_data, prod_data)
    region_correlation(middle_east, 'middle_east',food_data, prod_data)
    region_correlation(asia, 'asia',food_data, prod_data)
    region_correlation(africa, 'africa',food_data, prod_data)
    region_correlation(south_america, 'south_america',food_data, prod_data)
