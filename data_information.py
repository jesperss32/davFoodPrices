import eda
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

###############################
##	Import dataset
###############################
def loadingdata():
	df = pd.read_csv('firstclean_foodprices_data.csv', encoding='latin-1')
	#df = df.head(10000)
	return df

# This find the mean of every combination of product with country.
# This data is stored first in a numpy array, and this numpy array is loaded
# into a pandas dataframe.
def calculateinformation(countries, products, meanDataArray):
	for country in countries:
		#for product in products:
		product = "Bread"
		query = ('country == "{}" & _product == "{}"' .format(country, product))
		mean = eda.calcMean(df, query)
		if not np.isnan(mean):
			standardDeviation = eda.calcStandardDev(df, query)
			meanDataArray = np.append(meanDataArray, [[country, product, mean, standardDeviation]], axis=0)
			eda.boxPlot(df, query)
	return meanDataArray

# final shaping and presentation of the new dataframe
def shapeAndPresent(meanDataArray):
	meandf = pd.DataFrame(meanDataArray)
	meandf = meandf.drop(df.index[[0]])
	meandf.rename(columns={0: "country", 1: "product", \
		2: "mean", 3:"standard deviation"}, inplace = True)
	return meandf

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

#create array for addition data
meanDataArray = np.array([["", "", 0.11, 0.11]])

# main funtion
meanDataArray = calculateinformation(countries, products, meanDataArray)
metadf = shapeAndPresent(meanDataArray)
print(metadf)

print((metadf['standard deviation'].values.tolist()))

#plt.bar(len(metadf.index), metadf['standard deviation'])

plt.bar(metadf['country'], metadf['standard deviation'].astype(float))
plt.xticks(metadf['country'], rotation='vertical')
plt.show()




