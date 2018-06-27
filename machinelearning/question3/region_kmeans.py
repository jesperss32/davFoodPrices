import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from df_functions import get_data_selection, load_percentage_product_data, regions,\
    overlap_in_countries, getPriceLinkedProduct
from all_prod_price_region_cor import align_products_and_years
from sklearn.cluster import KMeans

def plot_all_data(region, food_data, prod_data):
    regionpricedata = get_data_selection(food_data, region)
    regionproddata = get_data_selection(prod_data, region)
    newfood, newprod = align_products_and_years(regionpricedata, regionproddata)
    products = newprod._product.unique().tolist()
    for product in products:
        newprod_product = newprod.loc[newprod['_product'] == product]
        linked = getPriceLinkedProduct(product)
        newfood_product = newfood.loc[newfood['_product'].isin(linked)]
        plt.scatter(newprod_product['value_change'], newfood_product['price_change'])
    plt.show()

def plot_product_year_country(fooddf, proddf, prodproduct, years):
    linked = getPriceLinkedProduct(prodproduct)
    fooddf = get_data_selection(fooddf, None, years, linked)
    proddf = get_data_selection(proddf, None, years, [prodproduct])
    fooddf, proddf = align_products_and_years(fooddf, proddf)
    countries = proddf.country.unique().tolist()
    for country in countries:
        newprod_product = proddf.loc[proddf['country'] == country]
        newfood_product = fooddf.loc[fooddf['country'] == country]
        plt.scatter(newprod_product['value_change'], newfood_product['price_change'])
    #plt.show()
    k = kmeans(fooddf, proddf, len(countries))
    plt.show()
def kmeans(newfood, newprod, N):
    X = np.array([newprod['value_change'],newfood['price_change']]).T
    kmeans = KMeans(n_clusters=N, random_state=0).fit(X)
    labels = kmeans.predict(X)
    #plt.scatter(newprod['value_change'], newfood['price_change'])
    print(kmeans.cluster_centers_)
    plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:,0])
    #plt.show()
    return kmeans




if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/country_year_average_percentage_data.csv')
    prod_data = load_percentage_product_data()
    europe, middle_east, asia, africa, south_america = regions()
    plot_product_year_country(food_data, prod_data, 'Maize', None)
