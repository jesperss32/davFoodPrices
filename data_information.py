import eda
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

###############################
##	Import dataset
###############################
# TODO: this is the raw datset, in the future the preprocessed dataset should be loaded
def loadingdata():
	df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

	df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
                   'mp_commoditysource' : 'source'}, inplace=True)
	#df = df.head(1000)
	return df


# This find the mean of every combination of product with country.
# This data is stored first in a numpy array, and this numpy array is loaded
# into a pandas dataframe.
def calculateinformation(countries, products, meanDataArray):
	for country in countries:
		for product in products:
			query = ('country == "{}" & _product == "{}"' .format(country, product))
			mean = eda.calcMean(df, query)
			print("check")
			if not np.isnan(mean):
				print("test")
				meanDataArray = np.append(meanDataArray, [[country, product, mean]], axis=0)
				print("found a mean, generation the price history plot now...")
				eda.boxPlot(df, query)
	#plt.show()
	return

# final shaping and presentation of the new dataframe
def shapeAndPresent(meanDataArray):
	meandf = pd.DataFrame(meanDataArray)
	meandf = meandf.drop(df.index[[0]])
	print(meandf)
	return

###############################
##	DataFrame
###############################
df = loadingdata()

###############################
##	Variables
###############################

#create list of all countries of the dataset
countries = list(set(df['country'].tolist()))

#creat a list of all products of the dataset
products = list(set(df['_product'].tolist()))

meanDataArray = np.array([["", "", 0.11]])

print("test")
calculateinformation(countries, products, meanDataArray)
shapeAndPresent(meanDataArray)






