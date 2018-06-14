import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
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
		prevN_inliers = N_inliers
		outliers = findOutliers(df, t)
	print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows (100 %)".format(t-1, t, df.shape[0]-prevN_inliers, round(float((df.shape[0]-prevN_inliers)*100)/df.shape[0], 1), df.shape[0]))

def boxPlot(dataFrame, query):
	dataFrame = dataFrame.query(query)
	fig = dataFrame.boxplot("price")
	print("figure created")
	#plt.show(fig)
	try: 
		fig.figure.savefig('plots/ "{}".png' .format(query))  # save the figure to file
	except:
		print("failed to save file")
	print("figure saved")
	plt.close()
	return



# Chart price history based on a query.
# For every unique currency included in the query, a different plot is generated.
# If such a plot includes multiple products, it takes the mean price of each product (from all countries)
# If such a plot includes only one product, it takes the mean price of the product per country (from all districts)
def chartPriceHistory(dataFrame, query):
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

				plt.plot(year_months, month_means, label=product)
			plt.legend()
			# plt.show()

		else:
			# for product in this_currency._product.unique():
			# 	print(product)
			# 	this_product = this_currency.query("_product==\"" + product + "\"")
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

				plt.plot(year_months, month_means, label=str(country)+", " + str(product))
			plt.legend()
	# plt.legend()
	plt.show()

if __name__ == '__main__':
	df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

	df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
	                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
	                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
	                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
	                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
	                   'mp_commoditysource' : 'source'}, inplace=True)

	query = 'currency=="USD"' 
	# fullEDA(df, query)
	# boxPlot(df, query)
	chartPriceHistory(df, query)