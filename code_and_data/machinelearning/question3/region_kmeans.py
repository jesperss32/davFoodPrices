import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from df_functions import get_data_selection, load_percentage_product_data, regions,\
    overlap_in_countries, getPriceLinkedProduct
from all_prod_price_region_cor import align_products_and_years
from sklearn.cluster import KMeans
from prod_price_cor_regions import year_country_average
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

def plot_product_year_country(fooddf, proddf, country, years):

    fooddf = get_data_selection(fooddf, [country], years, None)
    proddf = get_data_selection(proddf, [country], years, None)
    fooddf, proddf = align_products_and_years(fooddf, proddf)
    products = proddf._product.unique().tolist()
    print(products)
    for prod in products:
        #print(prod)
        linked = getPriceLinkedProduct(prod)
        if not linked:
            print('fail')
            continue
        newprod_product = proddf.loc[proddf['_product'] == prod]
        newfood_product = get_data_selection(fooddf, None, None, linked)
        newfood_product = year_country_average(newfood_product, 'price_change')
        print(len(newfood_product), len(newprod_product))
        plt.scatter(newprod_product['value_change'], newfood_product['price_change'])
    plt.show()
    k = kmeans(fooddf, proddf, 3)
    plt.show()
def kmeans(newfood, newprod, N):
    X = np.array([newprod['value_change'],newfood['price_change']]).T
    kmeans = KMeans(n_clusters=N, random_state=0).fit(X)
    labels = kmeans.predict(X)
    #plt.scatter(newprod['value_change'], newfood['price_change'])
    print(kmeans.cluster_centers_)
    #plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:,0])
    #plt.show()
    return kmeans




if __name__ == '__main__':
    food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/data/fooddatasets/country_year_average_percentage_data.csv')
    prod_data = load_percentage_product_data()
    europe, middle_east, asia, africa, south_america = regions()
    print(len(set(food_data.country.unique().tolist()).intersection(set(prod_data.country.unique().tolist()))))
    # for country in food_data.country.unique():
    #     print(country)
    #     print(len(food_data.loc[food_data['country'] == country]._product.unique()))
    # plot_product_year_country(food_data, prod_data, 'Rwanda', [2013])
