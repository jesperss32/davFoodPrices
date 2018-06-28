import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import numpy  as np
import matplotlib.dates as mdates
from df_functions import load_production_data, load_price_data, load_linked_data, getLinkedProduct, get_data_selection

def calcMean(dataFrame, query=None):
	if(query):
		dataFrame = dataFrame.query(query)
	return dataFrame.price.mean()

def calcStandardDev(dataFrame, query=None):
	if(query):
		dataFrame = dataFrame.query(query) 
	return dataFrame.price.std()

def findOutliers(dataFrame, threshold):
	mean = dataFrame.price.mean()
	stdev = dataFrame.price.std()
	abs_threshold = threshold * stdev
	mask = (dataFrame['price'] < mean - abs_threshold) | (dataFrame['price'] > mean + abs_threshold)
	return dataFrame[mask]

def nonGraphicalEDA(dataFrame, query): 
	df = dataFrame.query(query)
	print("Statistics for " + query + ":")
	print("Number of rows: {}".format(df.shape[0]))
	print("Mean price: {}".format(df.price.mean()))
	print("Standard Deviation: {}".format(df.price.std()))
	t = 1
	outliers = findOutliers(df, t)
	prevN_inliers = 0
	while outliers.shape[0] > 0:
		N_outliers = outliers.shape[0]
		N_inliers = df.shape[0] - N_outliers
		P_inliers_cumul = round(float(N_inliers * 100) / df.shape[0], 1)
		P_inliers = round(float((N_inliers-prevN_inliers) * 100) / df.shape[0], 1)
		print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows ({} %)".format(t-1, t, \
		       N_inliers-prevN_inliers, P_inliers, N_inliers, P_inliers_cumul))
		t = t + 1
		prevN_inliers = N_inliers
		outliers = findOutliers(df, t)
	print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows (100 %)".format(t-1, t, \
		   df.shape[0]-prevN_inliers, round(float((df.shape[0]-prevN_inliers)*100)/df.shape[0], 1), df.shape[0]))
	return

def boxPlot(dataFrame, query):
	dataFrame = dataFrame.query(query)
	dataFrame.boxplot("price")
	plt.show()
	return

# Chart price history based on a query.
# For every unique currency included in the query, a different plot is generated.
# If such a plot includes multiple products, it takes the mean price of each product (from all countries)
# If such a plot includes only one product, it takes the mean price of the product per country (from all districts)
def chartPriceHistory(dataFrame, query):
	dataFrame = dataFrame.query(query)
	unique_currencies = dataFrame.currency.unique()
	N_currencies = len(unique_currencies)
	rows = math.floor(math.sqrt(N_currencies))
	cols = math.ceil(N_currencies / rows)
	x = 1

	for currency in unique_currencies:
		plt.subplot(rows, cols, x)
		x = x + 1
		this_currency = dataFrame.query("currency == \"" + currency + "\"")
		unique_products = this_currency._product.unique()

		for product in unique_products:
			this_product = this_currency.query("_product==\"" + product + "\"")
			this_product = this_product.sort_values(by=['year', 'month'])
			month_means = []
			year_months = [] 
			for year in this_product.year.unique():
				this_year = this_product.query("year==" + str(year))
				print(this_year.country.unique())
				for month in this_year.month.unique():
					this_month = this_year.query("month==" + str(month))
					month_means.append(this_month.price.mean())
					year_months.append(dt.datetime(year=year, month=int(month), day=1))
			plt.plot(year_months, month_means, label=product + " (" + str(currency)+")")
			plt.legend()

	plt.show()
	return

def getYearMean(df, year): 
	df = df.query("year ==" + str(year))
	return df.price.mean()

def chartPriceProductionHistory(price_df, prod_df, links_df, product, country):
	price_df = price_df.query("_product== \"" + product + "\" & country==\"" + country + "\"")
	price_df = price_df.sort_values(by=['year', 'month'])
	month_means = []
	year_months = []
	for year in price_df.year.unique():
		this_year = price_df.query("year==" + str(year))
		for month in this_year.month.unique():
			this_month = this_year.query("month==" + str(month))
			month_means.append(this_month.price.mean())
			year_months.append(dt.datetime(year=year, month=int(month), day=1))

	linked_products = getLinkedProduct(product)
	for linked_prod in linked_products:
		prod_df = prod_df.query("_product == \"" + linked_prod + "\" & country == \"" + country + "\"")
		year_prods = []
		years = []
		for year in prod_df.year.unique():
			this_year = prod_df.query("year==" + str(year))
			year_prods.append((this_year.iloc[0]["value"]))
			years.append(dt.datetime(year=year, month=6, day= 30))

	fig, ax1 = plt.subplots()
	plt.title(str(country+", " + str(product)))
	ax1.plot(year_months, month_means, label=str(country)+", " + str(product), color='b')
	ax1.set_ylabel('Price', color='b')
	ax1.tick_params('y', colors='b')
	ax1.legend()

	ax2 = ax1.twinx()
	ax2.set_ylabel('Production (Tonnes)', color='r')
	ax2.plot(years, year_prods, label=str(country)+", " + str(product), color='r')
	ax2.legend()

	plt.legend()
	fig.tight_layout()
	plt.show()
	return

if __name__ == '__main__':
	price_df = load_price_data()
	prod_df = load_production_data()
	links_df = load_linked_data()

	query = 'country == "Lao People\'s Democratic Republic"'
	chartPriceHistory(price_df, query)
