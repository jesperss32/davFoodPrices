
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from operator import itemgetter
from scipy.stats import spearmanr
import os


def regions():
    middle_east = ['Afghanistan', 'Azerbaijan', 'Lebanon', 'Iran  (Islamic Republic of)', \
        'Iraq', 'Jordan', 'Syrian Arab Republic', 'Yemen', 'State of Palestine', \
        'South Sudan', 'Kyrgyzstan', 'Tajikistan']
    europe = ['Armenia', 'Georgia', 'Turkey', 'Ukraine']
    asia = ['Bangladesh', 'Cambodia', 'India', 'Indonesia', 'Lao People\'s Democratic Republic', \
        'Myanmar', 'Nepal', 'Pakistan', 'Philippines', 'Sri Lanka', 'Timor-Leste']
    africa = ['Benin', 'Central African Republic', 'Chad', 'Congo', 'Djibouti', \
        'Cameroon', 'Burkina Faso', 'Cape Verde', 'Cote d\'Ivoire', 'Democratic Republic of the Congo', \
        'Ethiopia', 'Gambia', 'Ghana', 'Guinea-Bissau', 'Guinea', 'Kenya', 'Madagascar', \
        'Malawi', 'Mali', 'Mauritania', 'Mozambique', 'Niger', 'Nigeria', 'Rwanda', \
        'Senegal', 'Somalia', 'Swaziland', 'Uganda', 'United Republic of Tanzania', \
        'Zambia', 'Zimbabwe', 'Sudan', 'Egypt', 'South Sudan', 'Burundi', 'Liberia', 'Lesotho']
    south_america = ['Bolivia', 'Colombia', 'Costa Rica', 'El Salvador', 'Guatemala', 'Haiti', 'Honduras', 'Panama', 'Peru']
    return europe, middle_east, asia, africa, south_america

def load_percentage_product_data():
    production_df = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/productiondata/production_percentage_data.csv', encoding='latin-1')
    production_df.rename(columns={'Area' : 'country', 'Item' : '_product', 'Year' : 'year', \
                        'Unit' : 'unit', 'Value' : 'value'}, inplace=True)
    return production_df


def getYearMean(df, year):
    df = df.query("year ==" + str(year))
    return df.price_change.mean()

def getLinkedProduct(product):
    linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', encoding='UTF-8', delimiter=";")
    prod = linked_products.query('price_df_product == \"' + product + '\"')
    return prod.production_df_product.unique()

def plotScatter(productionDf, priceDf, countries, priceProduct, region):
    priceDf = priceDf.query("_product==\"" + str(priceProduct) + '\"')
    priceDf = priceDf.loc[priceDf['country'].isin(countries)]
    #print(priceProduct)

    productionProducts = getLinkedProduct(priceProduct)
    #print(productionProducts)

    priceYears = priceDf.year.unique()
    for productionProduct in productionProducts:
        prodPerProdDf = productionDf.query('_product=="' + str(productionProduct) + '\"')
        prodPerProdDf = prodPerProdDf.loc[prodPerProdDf['country'].isin(countries)]
        productionYears = prodPerProdDf.year.unique()
        commonYears = list(set(priceYears).intersection(productionYears))
        productions = []
        prices = []
        for year in commonYears:
            yearlyProduction = prodPerProdDf.query('year=="' + str(year) + '"')
            productions.append(yearlyProduction.iloc[0]['value_change'])
            prices.append(getYearMean(priceDf, year))
        #print(commonYears)

        corr, pval = spearmanr(productions, prices)

        if pval <= 0.1 and (corr > 0.4 or corr < -0.4) :
            print('significant correlation detected between', priceProduct, 'and', productionProducts)
            print(corr, pval)
            # cwd = os.getcwd()
            # os.chdir('/home/student/Documents/Projecten/davFoodPrices/machinelearning/question3/correlated_region/corr0.4pvalue0.1')
            # save_df = pd.DataFrame({'production':productions, 'price': prices})
            # save_df.to_csv(region + '_'+priceProduct + '.csv')
            # os.chdir(cwd)
            # plt.scatter(productions, prices)
            # plt.title("Relation between {} price and {} production in {}".format(priceProduct, productionProduct, region))
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

def plotBest(minimum, region, rname):
    print(rname)
    combinations = [(22, 'India', 'Wheat', 'Wheat'), (21, 'Niger', 'Maize', 'Maize'), (21, 'Niger', 'Sorghum', 'Sorghum'), (16, 'Senegal', 'Sorghum', 'Sorghum'), (14, 'Afghanistan', 'Wheat', 'Wheat'), (14, 'Burkina Faso', 'Maize', 'Maize'), (14, 'Burkina Faso', 'Sorghum', 'Sorghum'), (14, 'Mozambique', 'Maize (white)', 'Maize'), (14, 'Nepal', 'Wheat', 'Wheat'), (14, 'Senegal', 'Maize (imported)', 'Maize'), (14, 'Tajikistan', 'Cabbage', 'Cabbages and other brassicas'), (14, 'Tajikistan', 'Carrots', 'Carrots and turnips'), (14, 'Tajikistan', 'Maize', 'Maize'), (14, 'Tajikistan', 'Potatoes', 'Potatoes'), (14, 'Tajikistan', 'Wheat', 'Wheat'), (13, 'Guatemala', 'Maize (white)', 'Maize'), (13, 'Guatemala', 'Maize (yellow)', 'Maize'), (13, 'Mali', 'Maize', 'Maize'), (13, 'Mali', 'Sorghum', 'Sorghum'), (12, 'Burundi', 'Cassava flour', 'Cassava'), (12, 'Burundi', 'Sweet potatoes', 'Sweet potatoes'), (12, 'Chad', 'Maize (white)', 'Maize'), (12, 'Chad', 'Sorghum (red)', 'Sorghum'), (12, 'Malawi', 'Maize', 'Maize'), (12, 'Mozambique', 'Beans (dry)', 'Beans, dry'), (11, 'Bangladesh', 'Lentils (masur)', 'Lentils'), (11, 'Colombia', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Beans (dry)', 'Beans, dry'), (11, 'Kenya', 'Maize (white)', 'Maize'), (11, 'Kenya', 'Potatoes (Irish)', 'Potatoes'), (11, 'Kenya', 'Sorghum', 'Sorghum'), (11, 'Kyrgyzstan', 'Potatoes', 'Potatoes'), (11, 'Peru', 'Potatoes', 'Potatoes'), (11, 'Tajikistan', 'Onions', 'Onions, dry'), (11, 'United Republic of Tanzania', 'Maize', 'Maize'), (11, 'Zambia', 'Maize (white)', 'Maize'), (10, 'Benin', 'Sorghum', 'Sorghum'), (10, 'Central African Republic', 'Cassava (cossette)', 'Cassava'), (10, 'Central African Republic', 'Maize', 'Maize'), (10, 'El Salvador', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Maize (white)', 'Maize'), (10, 'Ethiopia', 'Wheat', 'Wheat'), (10, 'Indonesia', 'Chili (green)', 'Chillies and peppers, green'), (10, 'Peru', 'Maize (local)', 'Maize'), (10, 'Senegal', 'Maize (local)', 'Maize')]
    relevant = [(c[1], c[2]) for c in combinations if c[1] in region]

    for i in range(len(relevant)):

        plotScatter(productionDf, priceDf, [r[0] for r in relevant], relevant[i][1], rname)


if __name__ == "__main__":
    linkedProductsDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/Linked_products.csv', encoding='UTF-8', delimiter=";")
    productionDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/productiondata/production_percentage_data.csv')
    priceDf = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/only_complete_years_data_percentages.csv', encoding='latin-1')
    europe, middle_east, asia, africa, south_america = regions()

    plotBest(10, europe, 'europe')
    plotBest(10, africa, 'africa')
    plotBest(10, asia, 'asia')
    plotBest(10, middle_east, 'middle_east')
    plotBest(10, south_america, 'south_america')
