
import pandas as pd
import csv

def get_years(df, country, product):
    relevant = df.loc[(df['country'] == country) & (df['_product'] == product)]
    years = relevant.year.unique().tolist()
    return years

def all_months(df, country, year, product):
    relevant = df.loc[(df['country'] == country) & (df['_product'] == product) \
                                                        & (df['year'] == year)]
    months = relevant.month.unique().tolist()
    if len(months) != 12:
        print('not complete with months', months)
        return False
    return True

# def handle_months(df, country, district, market, year, product):
#     relevant = df.loc[(df['country'] == country) & (df['_product'] == product) \
#                                                         & (df['year'] == year)]
#     months = relevant.month.unique().tolist()
#     if len(months) == 12:
#         return True, df
#     elif len(months) >= 10:
#         missing = [m for m in range(1, 12) if m not in months]
#         print(missing)
#         for m in missing:
#             if m-1 in months and m+1 in months:
#                 mm1 = df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == year)\
#                         & (df['month'] == m-1), 'price']
#                 mp1 = df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == year)\
#                         & (df['month'] == m+1),'price']
#                 new_p = (mm1.values[0]+mp1.values[0])/2
#                 row = df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == year)\
#                         & (df['month'] == m+1)]
#                 row['month'] = m
#                 row['price'] = new_p
#
#                 df = pd.concat([df.ix[:mm1.index.values[0]], row, df.ix[mp1.index.values[0]:]]).reset_index(drop=True)
#                 months.append(m)
#             elif m-1 == 0:
#                 prev_year = year-1
#                 prev_month = df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == prev_year)\
#                         & (df['month'] == 12), 'price']
#                 mp1 =  df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == year)\
#                         & (df['month'] == m+1),'price']
#                 if prev_month.any() and mp1.any():
#                     new_p = (prev_month.values[0] + mp1.values[0])/2
#                     row = df.loc[(df['country'] == country) & \
#                         (df['district'] == district) & (df['market'] == market) \
#                             & (df['_product'] == product) & (df['year'] == year)\
#                             & (df['month'] == 12)]
#                     row['month'] = m
#                     row['price'] = new_p
#
#                     df = pd.concat([df.ix[:prev_month.index.values[0]], row, df.ix[mp1.index.values[0]:]]).reset_index(drop=True)
#                     months.append(m)
#             elif m+1 == 13:
#                 next_year = year+1
#                 next_month = df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == prev_year)\
#                         & (df['month'] == 1), 'price']
#                 mm1 =  df.loc[(df['country'] == country) & \
#                     (df['district'] == district) & (df['market'] == market) \
#                         & (df['_product'] == product) & (df['year'] == year)\
#                         & (df['month'] == m-1),'price']
#                 if next_month.any() and mm.any():
#                     new_m = (next_month.values[0] + mm1.values[0])/2
#                     row = df.loc[(df['country'] == country) & \
#                         (df['district'] == district) & (df['market'] == market) \
#                             & (df['_product'] == product) & (df['year'] == year)\
#                             & (df['month'] == 1)]
#                     row['month'] = m
#                     row['price'] = new_p
#
#                     df = pd.concat([df.ix[:next_month.index.values[0]], row, df.ix[mm1.index.values[0]:]]).reset_index(drop=True)
#                     months.append(m)
#         if len(months) == 12:
#             return True, df
#         else:
#             return False, df
#
#     else:
#         return False, df


def handle_months_2(df, year):
    relevant = df.loc[df['year'] == year]
    months = relevant.month.unique().tolist()
    if len(months) == 12:
        # print('100%')
        # print(relevant)
        return True, df
    elif len(months) >= 10:
        missing = [m for m in range(1, 12) if m not in months]
        for m in missing:
            if m-1 in months and m+1 in months:
                mm1 = df.loc[df['month'] == m-1, 'price']
                mp1 = df.loc[df['month'] == m+1,'price']
                new_p = (mm1.values[0]+mp1.values[0])/2
                row = df.loc[df['month'] == m+1]
                row['month'] = m
                row['price'] = new_p
                print(mm1.index.values[0], mp1.index.values[0])
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
                    print(prev_month.index.values[0], mp1.index.values[0])
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
                    print(next_month.index.values[0],mm1.index.values[0])
                    df = pd.concat([df.ix[:next_month.index.values[0]], row, df.ix[mm1.index.values[0]:]]).reset_index(drop=True)
                    months.append(m)
        if len(months) == 12:
            print('adjusted')
            print(df.loc[df['year'] == year])
            return True, df
    return False, df


data = pd.read_csv('firstclean_foodprices_data.csv')
# prod1 = get_years(data, 'India', 'Rice')
# prod2 = get_years(data, 'India', 'Wheat')
# overlap = [x for x in prod1 if x in prod2]
# print([all_months(data, 'India', year, 'Rice') for year in overlap])


def interpolate_months(df):
    newdf = pd.DataFrame(columns = df.columns.values)
    countries = df.country.unique().tolist()
    for country in countries:
        country_d = df.loc[df['country'] == country]
        for district in country_d.district.unique().tolist():
            district_d = country_d.loc[country_d['district'] == district]
            for market in district_d.market.unique().tolist():
                market_d = district_d.loc[district_d['market'] == market]
                for product in market_d._product.unique().tolist():
                    product_d = market_d.loc[market_d['_product'] == product]
                    for year in product_d.year.unique.tolist():
                        complete, year_data = handle_months(df, country, district, market, year, product)
                        if complete:
                            newdf = newdf.append(year_data)
                        else:
                            print('discarded', product, 'in', year, 'for', country, district, market)
    return newdf


def compute_average_over_markets(df):
    print('runs')
    s = 0
    c = 0
    newdf = pd.DataFrame(columns = [x for x in df.columns.values if x != 'month'])
    countries = df.country.unique().tolist()
    for country in countries:
        districts = df.loc[df['country'] == country].district.unique().tolist()
        for dis in districts:
            markets = df.loc[(df['country'] == country) & (df['district'] == dis)].market.unique().tolist()
            for market in markets:
                products = df.loc[(df['country'] == country) & \
                    (df['district'] == dis) & (df['market'] == market)]._product.unique().tolist()
                for product in products:
                    years_market = df.loc[(df['country'] == country) & \
                        (df['district'] == dis) & (df['market'] == market) \
                            & (df['_product'] == product)]
                    years = years_market.year.unique().tolist()
                    for year in years:
                        complete, years_market = handle_months(years_market, country, dis, market, year, product)
                        print(complete, 'handled')
                        if complete:
                            year_average = years_market['price'].mean()
                            row = years_market.loc[years_market['year'] == year].iloc[0].drop('month')
                            row['price'] = year_average
                            newdf = newdf.append(row).reset_index(drop=True)
                        else:
                            s +=1

        c+=1
        print((c/len(countries)) * 100, '%')
    print('Deleted years:', s)
    return newdf

def compute_average_over_markets_2(df):
    print('runs')
    s = 0
    c = 0
    newdf = pd.DataFrame(columns = [x for x in df.columns.values if x != 'month'])
    markets = df.market_ID.unique().tolist()
    for market in markets:
        products = df.product_ID.unique().tolist()
        for product in products:
            years_market = df.loc[(df['market_ID'] == market) & (df['product_ID'] == product)]
            years = years_market.year.unique().tolist() # unique years
            for year in years:
                complete, this_years_market = handle_months_2(years_market, year)
                if complete:
                    if len(this_years_market.loc[this_years_market['year'] == year,'price']) != 12:
                        print('fail')
                        print(complete)
                        print(this_years_market.loc[this_years_market['year'] == year])
                        return
                    year_average = this_years_market.loc[this_years_market['year'] == year,'price'].mean()
                    row = this_years_market.loc[this_years_market['year'] == year].iloc[0].drop('month')
                    row['price'] = year_average
                    newdf = newdf.append(row).reset_index(drop=True)
                else:

                    s +=1
        return newdf
        c+=1
        print((c/len(markets)) * 100, '%')
    print('Deleted years:', s)
    return newdf


# print([x for x in data.columns.values if x != 'month'])
av = compute_average_over_markets_2(data)
av.to_csv('year_average_data.csv')
# for market in data.market.unique().tolist():
#     countries = data.loc[data['market'] == market].country.unique().tolist()
#     for country in countries
#     if len(countries) > 1:
#         print('duplicate market', market, countries)

# bread = data.loc[data['_product'] == 'Bread']
# print(len(bread.country.unique()))
