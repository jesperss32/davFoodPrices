import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from operator import itemgetter

def getYearMean(df, year):
	df = df.query("year ==" + str(year))
	return df.price.mean()

def getLinkedProduct(product):
	linked_products = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def plotScatter(productionDf, priceDf, country, priceProduct):
	priceDf = priceDf.query("_product==\"" + str(priceProduct) + "\" &country==\"" +str(country) + "\"")
	print(priceProduct)
	productionProducts = getLinkedProduct(priceProduct)
	print(productionProducts)

	priceYears = priceDf.year.unique()
	for productionProduct in productionProducts:
		prodPerProdDf = productionDf.query('Item=="' + str(productionProduct) + '"&Area=="'+str(country) + '"')
		productionYears = prodPerProdDf.Year.unique()
		commonYears = list(set(priceYears).intersection(productionYears))
		productions = []
		prices = []
		for year in commonYears:
		    yearlyProduction = prodPerProdDf.query('Year=="' + str(year) + '"')
		    productions.append(yearlyProduction.iloc[0]['Value'])
		    prices.append(getYearMean(priceDf, year))
		print(commonYears)
		plt.scatter(productions, prices)
		plt.title("Relation between {} price and {} production in {}".format(priceProduct, productionProduct, country))
		plt.xlabel('{} price'.format(priceProduct))
		plt.ylabel('{} production (tonnes)'.format(productionProduct))
		plt.show()
	return

def findBestProducts(minimumData):
    priceProducts = linkedProductsDf.price_df_product.unique()
    countries = productionDf.Area.unique()
    availableData = []
    for country in countries:
        for priceProduct in priceProducts:
            priceProductDf = priceDf.query("_product==\"" + str(priceProduct) + "\" &country==\"" +str(country) + "\"")
            priceYears = priceProductDf.year.unique()

            productionProducts = getLinkedProduct(priceProduct)
            for productionProduct in productionProducts:
                prodPerProdDf = productionDf.query('Item=="' + str(productionProduct) + '"&Area=="'+str(country) + '"')
                productionYears = prodPerProdDf.Year.unique()
                commonYearsLen = len(set(priceYears).intersection(productionYears))
                if commonYearsLen >= minimumData:
                    availableData.append((commonYearsLen, country, priceProduct, productionProduct))
    availableData.sort(key=itemgetter(0), reverse=True)
    print("There are {} products with these requirements".format(len(availableData)))
    return availableData

def plotBest(minimum):
	combinations = findBestProducts(minimum)
	for combination in combinations:
		print(combination)
		plotScatter(productionDf, priceDf, combination[1], combination[2])


if __name__ == "__main__":
	linkedProductsDf = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
	productionDf = pd.read_csv('cleaned_reduced_production.csv')
	priceDf = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')
	priceDf.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
	                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
	                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
	                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
	                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
	                   'mp_commoditysource' : 'source'}, inplace=True)


	plotBest(15)
