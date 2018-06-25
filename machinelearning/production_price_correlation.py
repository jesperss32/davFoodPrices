import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from df_functions import load_production_data, get_data_selection
from operator import itemgetter

def overlap_in_countries(food_data, prod_data):
    food_countries = food_data.country.unique()
    prod_countries = prod_data.country.unique()
    overlap = [c for c in food_countries if c in prod_countries]
    return sorted(overlap)

def overlap_in_years(food_data, prod_data):
    food_years = food_data.year.unique()
    prod_years = prod_data.year.unique()
    overlap = [y for y in food_years if y in prod_years]
    return sorted(overlap)

def get_matching_products(overlaps, fooddf_key):
    if fooddf_key in overlaps.keys():
        return overlaps[fooddf_key]
    return False

def getLinkedProduct(product):
	linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def overlapping_products():
    reader = csv.reader(open('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', 'r'), delimiter=';')
    proddf_pricedf = {}
    for row in reader:
        v, k = row
        proddf_pricedf[k] = v
    return proddf_pricedf


def compute_product_correlation(country, product, food_data, prod_data):
    overlap_years = overlap_in_years(food_data, prod_data)
    food_data_price = food_data.loc[food_data['year'].isin(overlap_years),'price']
    prod_data_production = prod_data.loc[prod_data['year'].isin(overlap_years), 'value']
    if not(prod_data_production.empty or food_data_price.empty):
        corr = spearmanr(prod_data_production, food_data_price)
        rho, pval = corr
        if pval <= 0.05:
            print(prod_data_production, food_data_price)
            # plt.scatter( prod_data_production, food_data_price)
            # plt.title(country + ' ' +product+ ' corr ' + str(rho) + ' pval ' + str(pval))
            # plt.xlabel('production')
            # plt.ylabel('price')
            # plt.show()
            return corr
    return False

def compute_correlations(food_data, prod_data):
    overlap_countries = overlap_in_countries(food_data, prod_data)
    overlap_years = overlap_in_years(food_data, prod_data)
    overlap_product_dict = overlapping_products()
    got_productiondata = overlap_product_dict.keys()
    matching = get_matching_products(overlap_product_dict, 'Maize')
    for country in overlap_countries:
        all_products = food_data.loc[food_data['country'] == country]._product.unique()
        available_products = [p for p in all_products if p in overlap_product_dict.keys()]
        for product in available_products:
            f_country_productdata = food_data.loc[(food_data['country'] == country) & (food_data['_product'] == product)]
            p_country_productdata = prod_data.loc[(prod_data['country'] == country) & (prod_data['_product'] == product)]
            corr = compute_product_correlation(country, product, f_country_productdata, p_country_productdata)
            if corr:
                rho,pval = corr
                print(country, product, 'corr=',rho, 'p=',pval)

def list_significant_correlations(food_data, prod_data):
    linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', delimiter=';')
    best_products = findBestProducts(10, linked_products, prod_data, food_data)
    sign_correlations = []
    for _, country, priceProduct, productionProduct in best_products:
        # products = get_data_selection(sign_food_data, [country])._product.unique()
        # for product in products:
        f_country_productdata = get_data_selection(food_data, [country], None, [priceProduct])
        p_country_productdata =get_data_selection(prod_data, [country], None, [productionProduct])
        corr = compute_product_correlation(country, priceProduct, f_country_productdata, p_country_productdata)
        if corr:
            rho,pval = corr
            # print(country, product, 'corr=',rho, 'p=',pval)
            sign_correlations.append((country, priceProduct, productionProduct))
    return sign_correlations


def findBestProducts(minimumData,linkedProductsDf,productionDf,priceDf):
    priceProducts = linkedProductsDf.price_df_product.unique()
    countries = productionDf.country.unique()
    availableData = []
    for country in countries:
        for priceProduct in priceProducts:
            priceProductDf = priceDf.query("_product==\"" + str(priceProduct) + "\" &country==\"" +str(country) + "\"")
            priceYears = priceProductDf.year.unique()

            productionProducts = getLinkedProduct(priceProduct)
            for productionProduct in productionProducts:
                prodPerProdDf = productionDf.query('_product=="' + str(productionProduct) + '"&country=="'+str(country) + '"')
                productionYears = prodPerProdDf.year.unique()
                commonYearsLen = len(set(priceYears).intersection(productionYears))
                if commonYearsLen >= minimumData:
                    availableData.append((commonYearsLen, country, priceProduct, productionProduct))
    availableData.sort(key=itemgetter(0), reverse=True)
    print("There are {} products with these requirements".format(len(availableData)))
    return availableData


if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/onlycountry_year_average_data.csv')
    # print(food_data.country.unique())
    # print(food_data.year.unique())
    prod_data = load_production_data()
    # print(production_data.year.unique())
    # print(production_data.country.unique())

    sign_cors = list_significant_correlations(food_data, prod_data)
    print(sign_cors)
    # print(overlap_countries)
    # print(overlap_years)
    # print(got_productiondata)
