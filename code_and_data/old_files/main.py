import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import Select
from bokeh.plotting import figure
import numpy as np 
import eda
from bokeh.client import push_session

# loading of dataset
def loadingpricedata():
	return pd.read_csv('data/firstclean_foodprices_data.csv', encoding='latin-1')

# data manupulation on the dataset, puts new data in new dataframe, now finding the:
# -- mean
# -- standard deviation
def gatherinformation(df, product):
	countries = list(set(df['country'].tolist()))
	dataArray = np.array([["", "", 0.11, 0.11]])
	for country in countries:
		query = ('country == "{}" & _product == "{}"' .format(country, product))
		mean = eda.calcMean(df, query)
		if not np.isnan(mean):
			standardDeviation = eda.calcStandardDev(df, query)
			dataArray = np.append(dataArray, [[country, product, mean, standardDeviation]], axis=0)

	dataArray = pd.DataFrame(dataArray)
	dataArray = dataArray.drop(df.index[[0]])
	dataArray.rename(columns={0: "country", 1: "product", \
		2: "mean", 3:"standard deviation"}, inplace = True)
	return dataArray	

# creates a bar plot of the standard deviation.
# using the bokeh library
def make_plot(product):
	subdf = gatherinformation(df, product)
	plot = figure(title = product, x_range= list(subdf['country']), y_range=(0, 1), width = 600, height = 600)
	plot.xaxis.major_label_orientation = np.pi/4
	plot.vbar(subdf['country'], width = 0.5, bottom = 0, top = subdf['standard deviation'])
	return plot

# If other plot is selected, it is updated overhere
def update_plot(atribute, old, new):
	plot2 = make_plot(new)
	layout.children.append(plot2)
	layout.children.pop(0)
	return




#
#	main program
#
df = loadingpricedata()
products = list(set(df['_product'].tolist()))
products.sort()
productselect = Select(title = "Select Product:", value = "Bread", options = products)

plot = productselect.on_change('value', update_plot)

output_file("standard_deviation.html")

plot = make_plot("Bread")
layout = column(children=[plot])

curdoc().add_root(column(widgetbox(productselect), layout))
session = push_session(curdoc())

curdoc().add_periodic_callback(update_plot, 1000)
session.show()
session.loop_until_closed()