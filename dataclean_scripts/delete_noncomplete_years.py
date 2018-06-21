import pandas as pd
import csv

def all_months(df, year):
    relevant = df.loc[df['year'] == year]
    months = relevant.month.unique().tolist()
    if len(months) != 12:
        return False
    return True


def handle_missing_months(df, year):
    relevant = df.loc[df['year'] == year]
    months = relevant.month.unique().tolist()
    if len(months) >= 10:
        missing = [m for m in range(1, 12) if m not in months]
        for m in missing:
            if m-1 in months and m+1 in months:
                mm1 = df.loc[df['month'] == m-1, 'price']
                mp1 = df.loc[df['month'] == m+1,'price']
                new_p = (mm1.values[0]+mp1.values[0])/2
                row = df.loc[df['month'] == m+1]
                row['month'] = m
                row['price'] = new_p
                df = pd.concat([df.ix[:mm1.index.values[0]], row, df.ix[mp1.index.values[0]:]]).reset_index(drop=True)
                months.append(m)
            elif m-1 == 0:
                prev_year = year-1
                prev_month = df.loc[ (df['year'] == prev_year)\
                        & (df['month'] == 12), 'price']
                mp1 =  df.loc[(df['year'] == year)\
                        & (df['month'] == m+1),'price']
                if prev_month.any() and mp1.any():
                    new_p = (prev_month.values[0] + mp1.values[0])/2
                    row = df.loc[(df['year'] == year)\
                            & (df['month'] == m+1)]
                    row['month'] = m
                    row['price'] = new_p
                    df = pd.concat([df.ix[:prev_month.index.values[0]], row, df.ix[mp1.index.values[0]:]]).reset_index(drop=True)
                    months.append(m)
            elif m+1 == 13:
                next_year = year+1
                next_month = df.loc[  (df['year'] == prev_year)\
                        & (df['month'] == 1), 'price']
                mm1 =  df.loc[ (df['year'] == year)\
                        & (df['month'] == m-1),'price']
                if next_month.any() and mm.any():
                    new_m = (next_month.values[0] + mm1.values[0])/2
                    row = df.loc[ (df['year'] == year)\
                            & (df['month'] == m-1)]
                    row['month'] = m
                    row['price'] = new_p
                    df = pd.concat([df.ix[:next_month.index.values[0]], row, df.ix[mm1.index.values[0]:]]).reset_index(drop=True)
                    months.append(m)
    if len(months) == 12:
        return True, df

    return False, df

def df_only_complete_years(df):
    print('RUNNING')
    s = 0
    c = 0
    # initialize new dataframe
    newdf = pd.DataFrame(columns = [x for x in df.columns.values if x != 'month'])
    # collect unique markets
    markets = df.market_ID.unique().tolist()
    for market in markets:
        # for each market collect products
        products = df.loc[df['market_ID'] == market].product_ID.unique().tolist()
        for product in products:
            # the market prices for each specific product
            market_production = df.loc[(df['market_ID'] == market) & (df['product_ID'] == product)]
            # years for which data is available
            years = market_production.year.unique().tolist()
            # for each year, compute average over months
            for year in years:
                year_data = market_production.loc[market_production['year'] == year]
                sales_methods = year_data.sale_ID.unique().tolist()
                # loop through all sales methods
                for sale in sales_methods:
                    sales_data = year_data.loc[year_data['sale_ID'] == sale]
                    # check if year is already complete
                    complete = all_months(sales_data, year)
                    if not complete:
                        # handle missing months
                        success, new_market_prod = handle_missing_months(sales_data, year)
                        if not success:
                            continue
                        # check if succesfully handled
                        if len(new_market_prod) != 12:
                            print('fail')
                            print(new_market_prod)
                            return
                        newdf = newdf.append(new_market_prod).reset_index(drop=True)
                    else:
                        newdf = newdf.append(sales_data).reset_index(drop=True)
                        print(sales_data)

        c+=1
        if int((c/len(markets) * 100)) %5  == 0:
            print((c/len(markets)) * 100, '%')
    return newdf

if __name__ == "__main__":
    data = pd.read_csv('secondclean_foodprices_data.csv')
    av = df_only_complete_years(data)
    av.to_csv('only_complete_years_data.csv')
