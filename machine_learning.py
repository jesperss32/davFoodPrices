import pandas as pd
import numpy as np
import csv
import random
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

def year_train_test_split(data, ratio):
    years = data.year.unique().tolist()
    all_indices = range(len(years))
    train_indices =  random.sample(range(len(years)), int(len(years) * ratio))
    train_years = [years[i] for i in train_indices]
    test_years = [years[i] for i in all_indices if i not in train_indices]
    train_data = data[data['year'].isin(train_years)]
    test_data = data[data['year'].isin(test_years)]
    return train_data, test_data


def monthly_predictions(df, country, product_ID):
    relevant_data = df.loc[(df['country'] == country) & (df['product_ID'] == product_ID)]
    trainset, testset = year_train_test_split(relevant_data, 0.7)

    train_labels = np.array(trainset['price']).reshape(-1,1)
    test_labels = np.array(testset['price']).reshape(-1,1)
    train_data = np.array(trainset['month']).reshape(-1,1)
    test_data = np.array(testset['month']).reshape(-1,1)

    regr = linear_model.LinearRegression()

    #
    # poly = PolynomialFeatures(2)
    # transform = poly.fit_transform(train_data)
    print(np.shape(train_data), np.shape(train_labels))

    regr.fit(train_data, train_labels)
    predict = regr.predict(test_data)
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(test_labels, predict))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(test_labels, predict))

    # Plot outputs
    plt.scatter(test_data, test_labels,  color='black')
    plt.plot(test_data, predict, color='blue', linewidth=3)
    plt.xlabel('month')
    plt.ylabel('price')
    plt.xticks(())
    plt.yticks(())

    plt.show()





if __name__ == "__main__":
    data = pd.read_csv('secondclean_foodprices_data.csv')
    av = monthly_predictions(data, 'India', 114)
    # 84 = wheat
    # 145 = rice low q
    # 114 = tomatoes
