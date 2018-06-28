import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from df_functions import load_production_data, load_percentage_product_data, get_data_selection
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
	linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()
#
# def overlapping_products():
#     reader = csv.reader(open('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', 'r'), delimiter=';')
#     proddf_pricedf = {}
#     for row in reader:
#         v, k = row
#         proddf_pricedf[k] = v
#     return proddf_pricedf


def compute_product_correlation(country, product, food_data, prod_data):
    overlap_years = overlap_in_years(food_data, prod_data)
    food_data_price = food_data.loc[food_data['year'].isin(overlap_years),'price_change']
    prod_data_production = prod_data.loc[prod_data['year'].isin(overlap_years), 'value']
    if not(prod_data_production.empty or food_data_price.empty):
        corr = spearmanr(prod_data_production, food_data_price)
        rho, pval = corr
        if pval <= 0.05:

            plt.scatter( prod_data_production, food_data_price)
            plt.title(country + ' ' +product+ ' corr ' + str(rho) + ' pval ' + str(pval))
            plt.xlabel('production')
            plt.ylabel('price')
            plt.show()
            return corr
    return False


def percentage_prod_price_correlation(product_df, price_df, plot=False):
    corr = spearmanr(product_df['value_change'], price_df['price_change'])
    rho, pvalue = corr
    # if pvalue <= 0.05:
    if plot:
        plt.scatter( product_df['value_change'], price_df['price_change'])
        plt.xlabel('Production change')
        plt.ylabel('Price change')
        plt.show()
    return corr
    return None

#
#
# def compute_correlations(food_data, prod_data):
#     overlap_countries = overlap_in_countries(food_data, prod_data)
#     overlap_years = overlap_in_years(food_data, prod_data)
#     overlap_product_dict = overlapping_products()
#     got_productiondata = overlap_product_dict.keys()
#     matching = get_matching_products(overlap_product_dict, 'Maize')
#     for country in overlap_countries:
#         all_products = food_data.loc[food_data['country'] == country]._product.unique()
#         available_products = [p for p in all_products if p in overlap_product_dict.keys()]
#         for product in available_products:
#             f_country_productdata = food_data.loc[(food_data['country'] == country) & (food_data['_product'] == product)]
#             p_country_productdata = prod_data.loc[(prod_data['country'] == country) & (prod_data['_product'] == product)]
#             corr = compute_product_correlation(country, product, f_country_productdata, p_country_productdata)
#             if corr:
#                 rho,pval = corr
#                 print(country, product, 'corr=',rho, 'p=',pval)

def list_significant_correlations(food_data, prod_data, best_products):
    sign_correlations = []
    for _, country, priceProduct, productionProduct in best_products:
        f_country_productdata = get_data_selection(food_data, [country], None, [priceProduct])
        p_country_productdata =get_data_selection(prod_data, [country], None, [productionProduct])
        overlap_years = overlap_in_years(f_country_productdata, p_country_productdata)
        f_country_productdata = get_data_selection(f_country_productdata, None, overlap_years, None)
        p_country_productdata =get_data_selection(p_country_productdata, None, overlap_years, None)
        corr = percentage_prod_price_correlation(p_country_productdata, f_country_productdata, plot=True)
        if corr:
            sign_correlations.append((country, priceProduct, productionProduct))
            production = p_country_productdata['value_change']
            price = f_country_productdata['price_change']
            save_df = pd.concat([production, price])
            save_df.to_csv(country + priceProduct + productionProduct + '.csv')

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
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/country_year_average_percentage_data.csv')
    # print(food_data.country.unique())
    # print(food_data.year.unique())
    prod_data = load_percentage_product_data()
    # print(production_data.year.unique())
    # print(production_data.country.unique())
    linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', delimiter=';')

    # best_products = findBestProducts(10, linked_products, prod_data, food_data)
    best_products = [(22, 'India', 'Wheat', 'Wheat'), (21, 'Niger', 'Maize', 'Maize'), (21, 'Niger', 'Sorghum', 'Sorghum'), (16, 'Senegal', 'Sorghum', 'Sorghum'), (14, 'Afghanistan', 'Wheat', 'Wheat'), (14, 'Burkina Faso', 'Maize', 'Maize'), (14, 'Burkina Faso', 'Sorghum', 'Sorghum'), (14, 'Mozambique', 'Maize (white)', 'Maize'), (14, 'Nepal', 'Wheat', 'Wheat'), (14, 'Senegal', 'Maize (imported)', 'Maize'), (14, 'Tajikistan', 'Cabbage', 'Cabbages and other brassicas'), (14, 'Tajikistan', 'Carrots', 'Carrots and turnips'), (14, 'Tajikistan', 'Maize', 'Maize'), (14, 'Tajikistan', 'Potatoes', 'Potatoes'), (14, 'Tajikistan', 'Wheat', 'Wheat'), (13, 'Guatemala', 'Maize (white)', 'Maize'), (13, 'Guatemala', 'Maize (yellow)', 'Maize'), (13, 'Mali', 'Maize', 'Maize'), (13, 'Mali', 'Sorghum', 'Sorghum'), (12, 'Burundi', 'Cassava flour', 'Cassava'), (12, 'Burundi', 'Sweet potatoes', 'Sweet potatoes'), (12, 'Chad', 'Maize (white)', 'Maize'), (12, 'Chad', 'Sorghum (red)', 'Sorghum'), (12, 'Malawi', 'Maize', 'Maize'), (12, 'Mozambique', 'Beans (dry)', 'Beans, dry'), (11, 'Bangladesh', 'Lentils (masur)', 'Lentils'), (11, 'Colombia', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Beans (dry)', 'Beans, dry'), (11, 'Kenya', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Potatoes (Irish)', 'Potatoes'), (11, 'Kenya', 'Sorghum', 'Sorghum'), (11, 'Kyrgyzstan', 'Potatoes', 'Potatoes'), (11, 'Peru', 'Potatoes', 'Potatoes'), (11, 'Tajikistan', 'Onions', 'Onions, dry'), (11, 'United Republic of Tanzania', 'Maize', 'Maize'), (11, 'Zambia', 'Maize (white)', 'Maize'), (10, 'Benin', 'Sorghum', 'Sorghum'), (10, 'Central African Republic', 'Cassava (cossette)', 'Cassava'), (10, 'Central African Republic', 'Maize', 'Maize'), (10, 'El Salvador', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Wheat', 'Wheat'), (10, 'Indonesia', 'Chili (green)', 'Chillies and peppers, green'), (10, 'Peru', 'Maize (local)', 'Maize'), (10, 'Senegal', 'Maize (local)', 'Maize')]

    sign_cors = list_significant_correlations(food_data, prod_data, best_products)
    print(sign_cors)
    # print(overlap_countries)
    # print(overlap_years)
    # print(got_productiondata)
