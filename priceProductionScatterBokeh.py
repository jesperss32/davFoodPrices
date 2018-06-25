import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import Select
from bokeh.plotting import figure
import numpy as np
import eda
from bokeh.client import push_session
from operator import itemgetter
from bokeh.models.widgets import Panel, Tabs

from numpy.random import random

def mscatter(p, x, y, marker):
    p.scatter(x, y, marker=marker, size=15,
              line_color="navy", fill_color="orange", alpha=0.5)

def mtext(p, x, y, text):
    p.text(x, y, text=[text],
           text_color="firebrick", text_align="center", text_font_size="10pt")

def getYearMean(df, year):
	df = df.query("year ==" + str(year))
	return df.price.mean()

def getLinkedProduct(product):
	linked_products = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def scatterLists(productionDf, priceDf, country, priceProduct):
    # make the figure
    p = figure(title="Relation between price and production", toolbar_location=None)
    p.grid.grid_line_color = 'Black'
    p.background_fill_color = "#eeeeee"

    priceDf = priceDf.query("_product==\"" + str(priceProduct) + "\" &country==\"" +str(country) + "\"")
    productionProducts = getLinkedProduct(priceProduct)

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
    return [productions, prices]

def plotBest(minimum):
    availableDataDf = pd.read_csv('scatterplotCandidates.csv')
    combinations = list(availableDataDf.itertuples(index=False))
    for combination in combinations:
    	if combination[1] >= minimum:
    		print(combination)
    		plotScatter(productionDf, priceDf, combination[2], combination[3])
    return

if __name__ == "__main__":
    linkedProductsDf = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
    productionDf = pd.read_csv('cleaned_reduced_production.csv')
    priceDf = pd.read_csv('data/firstclean_foodprices_data.csv', encoding='latin-1')
    priceDf.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
	                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
	                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
	                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
	                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
	                   'mp_commoditysource' : 'source'}, inplace=True)


    output_file("scatterplot.html", title="price/production scatter test")
    combinationSelection = [('India', 'Wheat'), ('Niger', 'Maize')]
    plot = 1
    for combination in combinationSelection:
        
    # make the figure
    p1 = figure(title="Relation between price and production", toolbar_location=None)
    p1.grid.grid_line_color = 'Black'
    p1.background_fill_color = "#eeeeee"
    scatterLists1 = scatterLists(productionDf, priceDf, 'India', 'Wheat')
    mscatter(p1, scatterLists1[0], scatterLists1[1], "circle")
    tab1 = Panel(child=p1, title='India' + '/' + 'Wheat')

    p2 = figure(title="Relation between price and production", toolbar_location=None)
    p2.grid.grid_line_color = 'Black'
    p2.background_fill_color = "#eeeeee"
    scatterLists2 = scatterLists(productionDf, priceDf, 'Niger', 'Maize')
    mscatter(p2, scatterLists2[0], scatterLists2[1], "circle")
    tab2 = Panel(child=p2, title='Niger' + '/' + 'Maize')

    tabs = Tabs(tabs=[tab1, tab2])


    show(tabs) # open a browser
