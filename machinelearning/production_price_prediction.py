import pandas as pd
import csv
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from production_price_correlation import load_production_data, \
        overlap_in_years,overlapping_products, list_significant_correlations
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

def years_train_test_split(data, ratio):
    years = data.year.unique()
    all_indices = range(len(years))
    train_indices =  random.sample(range(len(years)), int(len(years) * ratio))
    train_years = [years[i] for i in train_indices]
    test_years = [years[i] for i in all_indices if i not in train_indices]
    return train_years, test_years

def select_traintest_data(X_data, Y_data, training_years, testing_years):
    train_X = X_data[X_data['year'].isin(training_years)]
    test_X = X_data[X_data['year'].isin(testing_years)]
    train_Y = Y_data[Y_data['year'].isin(training_years)]
    test_Y = Y_data[Y_data['year'].isin(testing_years)]
    return train_X, train_Y, test_X, test_Y

def align_X_Y_data(food_data, prod_data, countries, products, years):
    relevant_food = food_data[(food_data['country'].isin(countries)) & \
        (food_data['_product'].isin(products)) & (food_data['year'].isin(years))]
    relevant_prod = prod_data[(prod_data['country'].isin(countries)) & \
        (prod_data['_product'].isin(products)) & (prod_data['year'].isin(years))]
    X_data = []
    Y_data = []
    s=0
    years = []
    for i, row in relevant_food.iterrows():
        country = row['country']
        product = overlapping_products()[row['_product']]
        year = row['year']
        years.append((year, country, product))
        prod_data_row = relevant_prod.loc[(relevant_prod['country'] == country) \
            & (relevant_prod['_product'] == product) & (relevant_prod['year'] == year)]
        if prod_data_row.shape[0] > 1:
            print('multiple selected')
            return False
        if prod_data_row.empty:
            s+=1
        X_data.append(prod_data_row['value'])
        Y_data.append(row['price'])
    X_Y_data = np.array([X_data, Y_data])
    print(list(set(years)))
    return X_Y_data


def linear_regression(X_Y_data, N):
    ''' Takes 2xn numpy array containing data and label in each column and
        predicts nth-order regression model '''
    trainyears, testyears = year_train_test_split(X_Y_data, 0.8)
    X_data = X_Y_data[0,:]
    Y_data = X_Y_data[1,:]
    train_labels = np.take(Y_data, trainyears, axis=1)
    test_labels = np.take(Y_data, testyears, axis=1)
    train_data = np.take(X_data, trainyears, axis=1)
    test_data = np.take(X_data, testyears, axis=1)

    regr = linear_model.LinearRegression()


    poly = PolynomialFeatures(N)
    transform_train = poly.fit_transform(train_data)
    transform_test = poly.fit_transform(test_data)
    regr.fit(transform_train, train_labels)
    predict = regr.predict(transform_test)
    return predict

if __name__ == '__main__':
    food_data = pd.read_csv('fooddatasets/onlycountry_year_average_data.csv')
    print(food_data.shape)
    prod_data = load_production_data()
    print(prod_data.shape)
    sign_years = overlap_in_years(food_data, prod_data)
    sign_cors = list_significant_correlations(food_data, prod_data)
    sign_countries = [x[0] for x in sign_cors]
    sign_prods = [x[1] for x in sign_cors]
    # food_data = food_data.loc[(food_data['country'] == 'Burkina Faso') & ( food_data['_product'] == 'Maize')]
    # prod_data = food_data.loc[(prod_data['country'] == 'Burkina Faso') & ( prod_data['_product'] == 'Maize')]

    align_X_Y_data(food_data, prod_data, sign_countries, sign_prods, sign_years)
