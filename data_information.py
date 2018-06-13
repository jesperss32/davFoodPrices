import eda
import pandas as pd 
import numpy as np 

###############################
##	Import dataset
###############################
# TODO: this is the raw datset, in the future the preprocessed dataset should be loaded

df = pd.read_csv('data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
                   'mp_commoditysource' : 'source'}, inplace=True)


###############################
##	Variables
###############################

#create list of all countries of the dataset
countries = list(set(df['country'].tolist()))

#creat a list of all products of the dataset
products = list(set(df['_product'].tolist()))

meanDataArray = np.array([["", "", 0.11]])


# This find the mean of every combination of product with country.
# This data is stored first in a numpy array, and this numpy array is loaded
# into a pandas dataframe.
for country in countries:
	for product in products:
		query = ('country == "{}" & _product == "{}"' .format(country, product))
		mean = eda.calcMean(df, query)
		if not np.isnan(mean):
			meanDataArray = np.append(meanDataArray, [[country, product, mean]], axis=0)

# final shaping and presentation of the new dataframe
meandf = pd.DataFrame(meanDataArray)
meandf = meandf.drop(df.index[[0]])
print(meandf)