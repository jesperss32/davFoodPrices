import pandas as pd
import csv

def compute_country_average(df):
    droplist = ['district', 'district_ID', 'market', 'market_ID']
    newdf = pd.DataFrame(columns = [x for x in df.columns.values if x not in droplist])
    countries = df.country_ID.unique().tolist()
    track = 0
    for country in countries:
        country_data = df.loc[df['country_ID'] == country]
        products = country_data.product_ID.unique().tolist()
        for product in products:
            prod_data = country_data.loc[country_data['product_ID'] == product]
            years = prod_data.year.unique().tolist()
            for year in years:
                yeardata = prod_data.loc[prod_data['year'] == year]
                average_price = yeardata['price'].mean()
                row = yeardata.iloc[0].drop(droplist)
                row['price'] = average_price
                newdf = newdf.append(row)
        track +=1
        print((track/len(countries))*100)
    return newdf


if __name__ == '__main__':
    data = pd.read_csv('nomr_yearly_average_data.csv')
    newdata = compute_country_average(data)
    newdata.to_csv('normr_country_year_average_data.csv')
