import pandas as pd

def load_production_data():
    '''Loads production table and renames its columns'''
    production_df = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/cleaned_reduced_production.csv', encoding='latin-1')
    production_df.rename(columns={'Area' : 'country', 'Item' : '_product', 'Year' : 'year', \
                        'Unit' : 'unit', 'Value' : 'value'}, inplace=True)
    return production_df


def getLinkedProduct(product):
	linked_products = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def overlap_in_countries(food_data, prod_data):
    food_countries = food_data.country.unique()
    prod_countries = prod_data.country.unique()
    overlap = [c for c in food_countries if c in prod_countries]
    return sorted(overlap)

def overlap_in_years(food_data, prod_data):
    food_years = food_data.year.unique()
    prod_years = prod_data.year.unique()
    overlap = [y for y in food_years if y in prod_years]
    return sorted(overlap)

def get_data_selection(df, countries=None, years=None, products=None):
    if countries:
        df = df.loc[df['country'].isin(countries)]
    if years:
        df = df.loc[df['year'].isin(years)]
    if products:
        df = df.loc[df['_product'].isin(products)]
    return df

def regions():
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
    rice = [p for p in products if 'rice' in p]
    print(rice, '\n')
    maize = [p for p in products if 'maize' in p]
    bread = [p for p in products if 'bread' in p]
    print(bread, '\n')
    meat = [p for p in products if 'meat' in p]+['poultry']
    print(meat, '\n')
    wheat= [p for p in products if 'wheat' in p ]
    print(wheat, '\n')
    livestock = [p for p in products if 'livestock' in p]
    print(livestock, '\n')
    beans = [p for p in products if 'bean' in p]
    print(beans, '\n')
    potatoes = [p for p in products if 'potatoes' in p]
    print(potatoes, '\n')
    lentils = [p for p in products if 'lentil' in p]
    print(lentils, '\n')
    milk_related = [p for p in products if 'milk' in p or 'cheese' in p] + ['butter']
    fish = [p for p in products if 'fish' in p]
    sugar = [p for p in products if 'sugar' in p]
    lists = rice+bread+meat+wheat+livestock+beans+potatoes+lentils+maize+milk_related\
        +fish+sugar
    print([p for p in products if p not in lists])

if __name__ == '__main__':
    food = pd.read_csv('/home/student/Documents/Projecten/davFoodPrices/fooddatasets/normr_country_year_average_data.csv')
    prod = load_production_data()
    products(food)
