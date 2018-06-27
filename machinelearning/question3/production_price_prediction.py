import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
# from production_price_correlation import overlap_in_years,overlapping_products,\
#                                                 list_significant_correlations
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from df_functions import get_data_selection, load_production_data, regions
import random
import os

def getLinkedProduct(product):
	linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def years_train_test_split_old(data, ratio):
    years = data.year.unique()
    all_indices = range(len(years))
    train_indices =  random.sample(range(len(years)), int(len(years) * ratio))
    train_years = [years[i] for i in train_indices]
    test_years = [years[i] for i in all_indices if i not in train_indices]
    return train_years, test_years

def years_train_test_split(data, ratio):
    np.random.shuffle(data)
    set_1_ind = int(len(data)*ratio)
    set_1 = data[:set_1_ind,:]
    set_1 = set_1[np.argsort(set_1[:, 0])]
    set_2 = data[set_1_ind:,:]
    set_2 = set_2[np.argsort(set_2[:,0])]
    return set_1,set_2


def align_X_Y_data(food_data, prod_data):
    X_data = []
    Y_data = []
    s=0
    years = []
    for i, row in food_data.iterrows():
        country = row['country']
        product = getLinkedProduct(row['_product'])
        year = row['year']
        years.append((year, country, product))
        prod_data_row = get_data_selection(prod_data, [country], [year], product)
        if prod_data_row.empty:
            continue
        if prod_data_row.shape[0] > 1:
            print('multiple selected')
            return False

        X_data.append(prod_data_row['value'].values.item())
        Y_data.append(row['price'])
    X_Y_data = np.array([X_data, Y_data]).T
    return X_Y_data


def linear_regression(X_Y_data, N):
    ''' Takes 2xn numpy array containing data and label in each column and
        predicts nth-order regression model '''
    # trainyears, testyears = years_train_test_split(X_Y_data, 0.8)
    # X_data_train = trainyears[:,0].reshape(-1,1)
    # Y_data_train = trainyears[:,1]
    # X_data_test = testyears[:,0].reshape(-1,1)
    # Y_data_test = testyears[:,1]
    traindata, testdata = years_train_test_split(X_Y_data, 0.8)
    X_data_train = traindata[:,0].reshape(-1,1)
    Y_data_train = traindata[:,1]
    X_data_test = testdata[:,0].reshape(-1,1)
    Y_data_test = testdata[:,1]

    regr = linear_model.LinearRegression()


    poly = PolynomialFeatures(N)
    transform_train = poly.fit_transform(X_data_train)
    transform_test = poly.fit_transform(X_data_test)
    regr.fit(transform_train, Y_data_train)
    predict_test = regr.predict(transform_test)
    predict_train = regr.predict(transform_train)
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(Y_data_test, predict_test))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(Y_data_test, predict_test))

    # Plot outputs
    f, (ax1, ax2) = plt.subplots(1, 2, sharex='all', sharey='all')
    ax1.scatter(X_data_test, Y_data_test,  color='black')
    ax1.plot(X_data_test, predict_test, color='blue', linewidth=2)
    ax1.set_xlabel('production value')
    ax1.set_ylabel('price')
    ax2.scatter(X_data_train, Y_data_train, color='black')
    ax2.plot(X_data_train, predict_train, color='blue', linewidth=2)

    ax1.set_title('Wheat in India: prediction')
    ax2.set_title('Wheat in India: fit')
    # plt.xticks(())
    # plt.yticks(())

    plt.show()
    return predict_test

def save_linear_regression_line(X_Y_data, N, filename):
    ''' Takes 2xn numpy array containing data and label in each column and
        predicts nth-order regression model '''
    # trainyears, testyears = years_train_test_split(X_Y_data, 0.8)
    # X_data_train = trainyears[:,0].reshape(-1,1)
    # Y_data_train = trainyears[:,1]
    # X_data_test = testyears[:,0].reshape(-1,1)
    # Y_data_test = testyears[:,1]
    traindata, testdata = years_train_test_split(X_Y_data, 0.5)
    # X_data_train = traindata[:,0].reshape(-1,1)
    # Y_data_train = traindata[:,1]
    # X_data_test = testdata[:,0].reshape(-1,1)
    # Y_data_test = testdata[:,1]

    X_data_train = X_Y_data[:,0].reshape(-1,1)
    X_data_test = X_Y_data[:,0].reshape(-1,1)
    Y_data_train = X_Y_data[:,1]
    Y_data_test = X_Y_data[:,1]

    regr = linear_model.LinearRegression()


    poly = PolynomialFeatures(N)
    transform_train = poly.fit_transform(X_data_train)
    transform_test = poly.fit_transform(X_data_test)
    regr.fit(transform_train, Y_data_train)
    predict = regr.predict(transform_test)
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(Y_data_test, predict))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(Y_data_test, predict))
    cwd = os.getcwd()
    os.chdir('/home/student/Documents/Projecten/davFoodPrices/machinelearning/question3/toPlotOnWebsite/regression_lines')
    df = pd.DataFrame({'production_data' : X_data_test.tolist(), 'predicted_price' : predict})
    df.to_csv(filename.replace('.csv', '') + 'linearmodel.csv')
    os.chdir(cwd)
    # Plot outputs
    # plt.scatter(X_data_test, Y_data_test,  color='black')
    # plt.plot(X_data_test, predict, color='blue', linewidth=2)
    # plt.xlabel('production value')
    # plt.ylabel('price')
    # plt.xticks(())
    # plt.yticks(())

    plt.show()
    return predict


if __name__ == '__main__':
    path = '/home/student/Documents/Projecten/davFoodPrices/machinelearning/question3/toPlotOnWebsite/region_corr_improved'
    cwd = os.getcwd()
    os.chdir(path)
    for filename in os.listdir(path):
        print(filename)
        df = pd.read_csv(filename)
        print(len(df))
        X_data = df.ix[:,0]
        Y_data = df.ix[:,1]
        X_Y_data = np.array(pd.concat([X_data, Y_data], axis=1))
        save_linear_regression_line(X_Y_data, 1, filename)
    os.chdir(cwd)
#
# if __name__ == '__main__':
#     food_data = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/onlycountry_year_average_data.csv')
#     prod_data = load_production_data()
#
#     # print(sign_years)
#     # sign_cors = list_significant_correlations(food_data, prod_data)
#     # print(sign_cors)
#     sign_cors = [('Senegal', 'Sorghum', 'Sorghum'), ('Burkina Faso', 'Maize', 'Maize'),\
#      ('Tajikistan', 'Cabbage', 'Cabbages and other brassicas'), ('Tajikistan', 'Carrots',\
#       'Carrots and turnips'), ('Tajikistan', 'Maize', 'Maize'), ('Tajikistan', 'Potatoes',\
#        'Potatoes'), ('Tajikistan', 'Wheat', 'Wheat'), ('Guatemala', 'Maize (white)', 'Maize'), \
#        ('Guatemala', 'Maize (yellow)', 'Maize'), ('Mali', 'Maize', 'Maize'), \
#        ('Kenya', 'Beans (dry)', 'Beans, dry'), ('Kenya', 'Maize (white)', 'Maize'), \
#        ('Kenya', 'Sorghum', 'Sorghum'), ('Peru', 'Potatoes', 'Potatoes'),\
#         ('Tajikistan', 'Onions', 'Onions, dry'), ('Zambia', 'Maize (white)', 'Maize'),\
#          ('Indonesia', 'Chili (green)', 'Chillies and peppers, green'), \
#          ('Peru', 'Maize (local)', 'Maize')]
#
#     sign_countries = [x[0] for x in sign_cors]
#     sign_priceProd = [x[1] for x in sign_cors]
#     sign_prodProd = [x[2] for x in sign_cors]
#     sign_years = overlap_in_years(food_data, prod_data)
#     relevant_food = get_data_selection(food_data, sign_countries, sign_years, sign_priceProd)
#     relevant_prod = get_data_selection(prod_data, sign_countries, sign_years, sign_prodProd)
#     # print(get_data_selection(relevant_prod, ['Burkina Faso'], [2003], ['Maize']))
#     # food_data = food_data.loc[(food_data['country'] == 'Burkina Faso') & ( food_data['_product'] == 'Maize')]
#     # prod_data = food_data.loc[(prod_data['country'] == 'Burkina Faso') & ( prod_data['_product'] == 'Maize')]
#     europe, middle_east, asia, africa = regions()
#     europe_cluster = []
#     middle_east_cluster = []
#     asia_cluster = []
#     africa_cluster = []
#     for i in sign_cors:
#         country = i[0]
#         if country in europe:
#             europe_cluster.append(country)
#         elif country in asia:
#             asia_cluster.append(country)
#         elif country in africa:
#             africa_cluster.append(country)
#         elif country in middle_east:
#             middle_east_cluster.append(country)
#     europe_cluster = list(set(europe_cluster))
#     asia_cluster = list(set(asia_cluster))
#     africa_cluster = list(set(asia_cluster))
#     middle_east_cluster = list(set(middle_east_cluster))
#     print(middle_east_cluster)
#         # country = i[0]
#         # fp = i[1]
#         # pp = i[2]
#         # sen_sor_food = get_data_selection(relevant_food, [country], None, [fp])
#         # sen_sor_prod = get_data_selection(relevant_prod, [country], None, [pp])
#         # X_Y_data = align_X_Y_data(sen_sor_food, sen_sor_prod)
#         # linear_regression(X_Y_data, 1)
