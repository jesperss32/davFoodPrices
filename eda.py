import pandas as pd

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
	while outliers.shape[0] > 0:
		N_outliers = outliers.shape[0]
		N_inliers = df.shape[0] - N_outliers
		P_inliers = round(N_inliers / df.shape[0] * 100, 1)
		print("Rows within {} standard deviations: {} ({}%)".format(t, N_inliers, P_inliers))
		t = t + 1
		outliers = findOutliers(df, t)
	print("Rows within {} standard deviations: {} (100 %)".format(t, df.shape[0]))


df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
                   'mp_commoditysource' : 'source'}, inplace=True)


query = 'country == "Afghanistan"'

fullEDA(df, query)