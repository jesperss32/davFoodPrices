import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from operator import itemgetter
from scipy.stats import spearmanr
import os


def load_percentage_product_data():
    production_df = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/productiondata/production_percentage_data.csv', encoding='latin-1')
    production_df.rename(columns={'Area' : 'country', 'Item' : '_product', 'Year' : 'year', \
                        'Unit' : 'unit', 'Value' : 'value'}, inplace=True)
    return production_df


def getYearMean(df, year):
    df = df.query("year ==" + str(year))
    return df.price.mean()

def getLinkedProduct(product):
    linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', encoding='UTF-8', delimiter=";")
    prod = linked_products.query('price_df_product == \"' + product + '\"')
    return prod.production_df_product.unique()

def plotScatter(productionDf, priceDf, country, priceProduct):
    priceDf = priceDf.query("_product==\"" + str(priceProduct) + "\" &country==\"" +str(country) + "\"")
    #print(priceProduct)
    productionProducts = getLinkedProduct(priceProduct)
    #print(productionProducts)

    priceYears = priceDf.year.unique()
    for productionProduct in productionProducts:
        prodPerProdDf = productionDf.query('_product=="' + str(productionProduct) + '"&country=="'+str(country) + '"')
        productionYears = prodPerProdDf.year.unique()
        commonYears = list(set(priceYears).intersection(productionYears))
        productions = []
        prices = []
        for year in commonYears:
            yearlyProduction = prodPerProdDf.query('year=="' + str(year) + '"')
            productions.append(yearlyProduction.iloc[0]['value'])
            prices.append(getYearMean(priceDf, year))
        #print(commonYears)

        corr, pval = spearmanr(productions, prices)

        if pval <= 0.05 and (corr > 0.4 or corr < -0.4) :
            print('significant correlation detected between', priceProduct, 'and', productionProducts)
            print(country)
            print(corr, pval)
            cwd = os.getcwd()
            os.chdir('/home/student/Documents/Projecten/davFoodPrices/machinelearning/question3/correlated_country')
            save_df = pd.DataFrame({'production':productions, 'price': prices})
            save_df.to_csv(country + '_'+priceProduct + '.csv')
            os.chdir(cwd)
            # plt.scatter(productions, prices)
            # plt.title("Relation between {} price and {} production in {}".format(priceProduct, productionProduct, country))
            # plt.xlabel('{} production change'.format(productionProduct))
            # plt.ylabel('{} price change (tonnes)'.format(priceProduct))
            # plt.show()
    return

def findBestProducts(minimumData):
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

def plotBest(minimum):
    combinations = [(22, 'India', 'Wheat', 'Wheat'), (21, 'Niger', 'Maize', 'Maize'), (21, 'Niger', 'Sorghum', 'Sorghum'), (16, 'Senegal', 'Sorghum', 'Sorghum'), (14, 'Afghanistan', 'Wheat', 'Wheat'), (14, 'Burkina Faso', 'Maize', 'Maize'), (14, 'Burkina Faso', 'Sorghum', 'Sorghum'), (14, 'Mozambique', 'Maize (white)', 'Maize'), (14, 'Nepal', 'Wheat', 'Wheat'), (14, 'Senegal', 'Maize (imported)', 'Maize'), (14, 'Tajikistan', 'Cabbage', 'Cabbages and other brassicas'), (14, 'Tajikistan', 'Carrots', 'Carrots and turnips'), (14, 'Tajikistan', 'Maize', 'Maize'), (14, 'Tajikistan', 'Potatoes', 'Potatoes'), (14, 'Tajikistan', 'Wheat', 'Wheat'), (13, 'Guatemala', 'Maize (white)', 'Maize'), (13, 'Guatemala', 'Maize (yellow)', 'Maize'), (13, 'Mali', 'Maize', 'Maize'), (13, 'Mali', 'Sorghum', 'Sorghum'), (12, 'Burundi', 'Cassava flour', 'Cassava'), (12, 'Burundi', 'Sweet potatoes', 'Sweet potatoes'), (12, 'Chad', 'Maize (white)', 'Maize'), (12, 'Chad', 'Sorghum (red)', 'Sorghum'), (12, 'Malawi', 'Maize', 'Maize'), (12, 'Mozambique', 'Beans (dry)', 'Beans, dry'), (11, 'Bangladesh', 'Lentils (masur)', 'Lentils'), (11, 'Colombia', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Beans (dry)', 'Beans, dry'), (11, 'Kenya', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Potatoes (Irish)', 'Potatoes'), (11, 'Kenya', 'Sorghum', 'Sorghum'), (11, 'Kyrgyzstan', 'Potatoes', 'Potatoes'), (11, 'Peru', 'Potatoes', 'Potatoes'), (11, 'Tajikistan', 'Onions', 'Onions, dry'), (11, 'United Republic of Tanzania', 'Maize', 'Maize'), (11, 'Zambia', 'Maize (white)', 'Maize'), (10, 'Benin', 'Sorghum', 'Sorghum'), (10, 'Central African Republic', 'Cassava (cossette)', 'Cassava'), (10, 'Central African Republic', 'Maize', 'Maize'), (10, 'El Salvador', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Wheat', 'Wheat'), (10, 'Indonesia', 'Chili (green)', 'Chillies and peppers, green'), (10, 'Peru', 'Maize (local)', 'Maize'), (10, 'Senegal', 'Maize (local)', 'Maize')]
    #combinations = findBestProducts(5)
    for combination in combinations:
        #print(combination)
        plotScatter(productionDf, priceDf, combination[1], combination[2])


if __name__ == "__main__":
    linkedProductsDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', encoding='UTF-8', delimiter=";")
    productionDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/productiondata/production_percentage_data.csv')
    priceDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/only_complete_years_data_percentages.csv', encoding='latin-1')
    priceDf.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
                       'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
                       'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
                       'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
                       'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
                       'mp_commoditysource' : 'source'}, inplace=True)


    plotBest(10)
