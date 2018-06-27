import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from df_functions import load_percentage_product_data, get_data_selection, regions,\
    getLinkedProduct, overlap_in_years, overlap_in_countries, getPriceLinkedProduct
from operator import itemgetter
from prod_price_cor_regions import get_overlapping_data, year_average, \
    align_years, correlation, year_country_average

def align_products_and_years(fooddf, proddf):
    newfooddf = pd.DataFrame(columns=fooddf.columns.values)
    newproddf = pd.DataFrame(columns=proddf.columns.values)
    products = [p for p in proddf._product.unique().tolist() if getPriceLinkedProduct(p)]
    for product in products:
        #print('product',product)
        linked = getPriceLinkedProduct(product)
        #print('linked', linked)
        #print(product, linked)
        productprice = get_data_selection(fooddf, None, None, linked)
        #print('product priceentries', len(productprice))
        productprod = get_data_selection(proddf, None, None, [product])
        #print('product productionentries', len(productprod))
        countries = overlap_in_countries(productprice, productprod)
        #print(countries, 'have this product data')
        productprice = get_data_selection(productprice, countries)
        productprod = get_data_selection(productprod, countries)
        #print(' this leaves product priceentries', len(productprice))
        #print('product productionentries', len(productprod))
        #print(len(productprice), linked, 'entries')
        overlapyears = overlap_in_years(productprice, productprod)
        productprice = get_data_selection(productprice, None, overlapyears)
        productprod = get_data_selection(productprod, None, overlapyears)
        #print(sorted(productprice.year.unique().tolist()) == sorted(productprod.year.unique().tolist())
        newfood, newprod = align_years(productprice, productprod)
        if len(newfood._product.unique()) != len(newprod._product.unique()):
            newfood = year_country_average(newfood, 'price_change')
        #print('Equal dataframes:', len(newfood) == len(newprod))
        if not len(newfood) == len(newprod):
            newprod, newfood = get_overlapping_data(newprod, newfood)
            #
            # if not sorted(newfood.year.unique().tolist()) == sorted(newprod.year.unique().tolist()):
            #     print('years misaligned')
            # if not (len(newfood.country.unique()) == len(newprod.country.unique())):
            #     print('countries misaligned')
            # if not (len(newfood._product.unique()) == len(newprod._product.unique())):
            #     print('product error')
            #     print(sorted(newprod.country.tolist()) == sorted(newfood.country.tolist()))
            #     break
            #print(' now Equal dataframes:', len(newfood) == len(newprod))
        newfooddf = newfooddf.append(newfood)
        newproddf = newproddf.append(newprod)
    return newfooddf, newproddf



def all_products_region_correlation(region, reg_name, food_data, prod_data):
    region_pricedata = get_data_selection(food_data, region)
    region_proddata = get_data_selection(prod_data, region)

    overlap_countries = overlap_in_countries(region_pricedata, region_proddata)
    region_price = get_data_selection(region_pricedata, overlap_countries)
    region_production = get_data_selection(region_proddata, overlap_countries)

    newfood, newprod = align_products_and_years(region_price, region_production)
    print(len(newfood), len(newprod))
    corr = correlation(newprod, newfood)
    if corr:
        rho, pvalue=corr
        print(rho, pvalue)
        print(reg_name)
        save_df = pd.concat([newprod['value_change'], newfood['price_change']])
        save_df.to_csv(reg_name + '.csv')


if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/country_year_average_percentage_data.csv')
    prod_data = load_percentage_product_data()
    europe, middle_east, asia, africa, south_america = regions()
    all_products_region_correlation(europe, 'europe', food_data, prod_data)
    all_products_region_correlation(middle_east, 'middle_east',food_data, prod_data)
    all_products_region_correlation(asia, 'asia',food_data, prod_data)
    all_products_region_correlation(africa, 'africa',food_data, prod_data)
    all_products_region_correlation(south_america, 'south_america',food_data, prod_data)
