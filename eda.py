import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import numpy  as np
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
	

def fullEDA(dataFrame, query): 
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
		print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows ({} %)".format(t-1, t, N_inliers-prevN_inliers, P_inliers, N_inliers, P_inliers_cumul))
		t = t + 1
		prevN_inliers = N_inliersn
		outliers = findOutliers(df, t)
	print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows (100 %)".format(t-1, t, df.shape[0]-prevN_inliers, round(float((df.shape[0]-prevN_inliers)*100)/df.shape[0], 1), df.shape[0]))

def boxPlot(dataFrame, query):
	dataFrame = dataFrame.query(query)
	dataFrame.boxplot("price")
	plt.show()



# Chart price history based on a query.
# For every unique currency included in the query, a different plot is generated.
# If such a plot includes multiple products, it takes the mean price of each product (from all countries)
# If such a plot includes only one product, it takes the mean price of the product per country (from all districts)
def chartPriceHistory(dataFrame, query, ax=None):
	dataFrame = dataFrame.query(query)
	unique_currencies = dataFrame.currency.unique()
	N_currencies = len(unique_currencies)
	print(N_currencies)
	rows = math.floor(math.sqrt(N_currencies))
	cols = math.ceil(N_currencies / rows)
	x = 1
	for currency in unique_currencies:
		print(currency, x)
		plt.subplot(rows, cols, x)
		x = x + 1
		this_currency = dataFrame.query("currency == \"" + currency + "\"")
		unique_products = this_currency._product.unique()

		if len(unique_products) > 1:
			for product in unique_products:
				print(product)
				this_product = this_currency.query("_product==\"" + product + "\"")
				this_product = this_product.sort_values(by=['year', 'month'])
				month_means = []
				year_months = [] 
				for year in this_product.year.unique():
					this_year = this_product.query("year==" + str(year))
					print(year)
					for month in this_year.month.unique():
						this_month = this_year.query("month==" + str(month))
						print(month)
						month_means.append(this_month.price.mean())
						year_months.append(dt.datetime(year=year, month=month, day=1))
				if(ax):
					plt.plot(year_months, month_means, label=product, ax=ax)
				else:
					country = this_currency.country.unique()[0]
					plt.plot(year_months, month_means, label=str(country)+", " + str(product))
			plt.legend()
			# plt.show()

		else:
			for product in this_currency._product.unique():
				print(product)
				this_product = this_currency.query("_product==\"" + product + "\"")
				for country in this_product.country.unique():
					print(country)
					this_country = this_product.query("country==\"" + country + "\"")
					this_country = this_country.sort_values(by=['year', 'month'])
					month_means = []
					year_months = []
					for year in this_country.year.unique():
						this_year = this_country.query("year==" + str(year))
						for month in this_year.month.unique():
							this_month = this_year.query("month==" + str(month))
							month_means.append(this_month.price.mean())
							year_months.append(dt.datetime(year=year, month=month, day=1))
				if(ax):
					ax.plot(year_months, month_means, label=str(country)+", " + str(product))
				else:
					plt.plot(year_months, month_means, label=str(country)+", " + str(product))
			plt.legend()
	plt.legend()
	plt.show()
	return

def getMissingYears(df):
	years = sorted(df.Year.unique())
	missing_years = []
	# print("Years: {}".format(df.Year.unique()))
	for year in range(min(years), max(years)):
		if not year in years:
			missing_years.append(year)
	# print("Missing years: {}".format(missing_years))
	return missing_years

def getProductionStats(df, query):
	df = df.query(query)
	print("Statistics for " + query + ":")
	print("Number of rows: {}".format(df.shape[0]))
	print("Mean production: {}".format(df.Value.mean()))
	print("Standard Deviation: {}".format(df.Value.std()))
	print(getMissingYears(df))
	return

def findAllMissingYears(df):
	countries = df.Area.unique()
	for country in countries:
		this_country = df.query("Area ==\"" + country + "\"")
		products = this_country.Item.unique()
		for product in products:
			this_product = this_country.query("Item == \"" + product + "\"")
			missing_years = getMissingYears(this_product)
			if missing_years:
				print("Missing years for ({}, {}): {}".format(country, product, missing_years))

def getLinkedProducts(product):
	linked_products = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

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
			year_months.append(dt.datetime(year=year, month=month, day=1))

	linked_products = getLinkedProducts(product)
	print(linked_products)
	for linked_prod in linked_products:
		prod_df = prod_df.query("Item == \"" + linked_prod + "\" & Area == \"" + country + "\"")
		year_prods = []
		years = []
		for year in prod_df.Year.unique():
			this_year = prod_df.query("Year==" + str(year))
			year_prods.append((this_year.iloc[0]["Value"]))
			years.append(dt.datetime(year=year, month=6, day= 30))

	fig, ax1 = plt.subplots()
	ax1.plot(year_months, month_means, label=str(country)+", " + str(product))
	ax1.set_ylabel('Price', color='b')
	ax1.tick_params('y', colors='b')

	ax2 = ax1.twinx()
	ax2.set_ylabel('Production (Tonnes)')
	ax2.plot(years, year_prods, label=str(country)+", " + str(product))

	fig.tight_layout()
	plt.show()
	return

if __name__ == '__main__':
	price_df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

	price_df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
	                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
	                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
	                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
	                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
	                   'mp_commoditysource' : 'source'}, inplace=True)

	prod_df = pd.read_csv('cleaned_reduced_production.csv')

	links_df = pd.read_csv('Linked_products.csv', delimiter=";")

	# findAllMissingYears(prod_df)

	# getProductionStats(prod_df, "Area == \"Afghanistan\" & Item == \"Cotton lint\"")

	chartPriceProductionHistory(price_df, prod_df, links_df, "Wheat", "Nepal")

	chartPriceHistory(price_df, "country == \"Nepal\" & (_product == \"Wheat\" | _product == \"Rice\")")