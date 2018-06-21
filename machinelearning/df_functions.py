import pandas as pd

def load_production_data():
    '''Loads production table and renames its columns'''
    production_df = pd.read_csv('/home/student/Documents/Projecten/cleaned_reduced_production.csv', encoding='latin-1')
    production_df.rename(columns={'Area' : 'country', 'Item' : '_product', 'Year' : 'year', \
                        'Unit' : 'unit', 'Value' : 'value'}, inplace=True)
    return production_df

def get_data_selection(df, countries, years, products):
    if countries:
        df = df.loc[df['country'].isin(countries)]
    if years:
        df = df.loc[df['year'].isin(years)]
    if products:
        df = df.loc[df['_product'].isin(products)]
    return df

def regions(df):
    middle_east = ['Afghanistan', 'Azerbaijan', 'Lebanon', 'Iran  (Islamic Republic of)', \
        'Iraq', 'Jordan', 'Syrian Arab Republic', 'Yemen', 'State of Palestine', \
        'South Sudan', 'Kyrgyzstan', 'Tajikistan']
    europe = ['Armenia', 'Georgia', 'Turkey', 'Ukraine']
    asia = ['Bangladesh', 'Cambodia', 'India', 'Indonesia', 'Lao People\'s Democratic Republic', \
        'Myanmar', 'Nepal', 'Pakistan', 'Philippines', 'Sri Lanka', 'Timor-Leste']
    africa = ['Benin', 'Central African Republic', 'Chad', 'Congo', 'Djibouti', \
        'Cameroon', 'Burkina Faso', 'Cape Verde', 'Cote d\'Ivoire', 'Democratic Republic of the Congo', \
        'Ethiopia', 'Gambia', 'Ghana', 'Guinea-Bissau', 'Guinea', 'Kenya', 'Madagascar', \
        'Malawi', 'Mali', 'Mauritania', 'Mozambique', 'Niger', 'Nigeria', 'Rwanda', \
        'Senegal', 'Somalia', 'Swaziland', 'Uganda', 'United Republic of Tanzania', \
        'Zambia', 'Zimbabwe', 'Sudan', 'Egypt', 'South Sudan', 'Burundi', 'Liberia', 'Lesotho']
    south_america = ['Bolivia', 'Colombia', 'Costa Rica', 'El Salvador', 'Guatemala', 'Haiti', 'Honduras', 'Panama', 'Peru']
    return europe, middle_east, asia, africa

def products(df):
    products = [p.lower() for p in df._product.unique()]
    rice_related = [p for p in products if 'rice' in p]
    bread_related = [p for p in products if 'bread' in p]
    meat_related = [p for p in products if 'meat' in p]
    wheat_related = [p for p in products if 'wheat' in p ]
    livestock = [p for p in products if 'livestock' in p]
    beans = [p for p in products if 'bean' in p]
    print([p for p in products if p not in rice_related and p not in bread_related \
        and p not in meat_related and p not in wheat_related and p not in livestock \
        and p not in beans])


if __name__ == '__main__':
    food = pd.read_csv('fooddatasets/onlycountry_year_average_data.csv')
    prod = load_production_data()
    products(food)
