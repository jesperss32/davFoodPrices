import pandas as pd
import numpy as np
import csv
from df_functions import get_data_selection, load_price_data, overlap_in_years, overlap_in_countries
from scipy.stats import spearmanr
from math import isnan

def all_combinations(lst):
    result = []
    for p1 in range(len(lst)):
            for p2 in range(p1+1,len(lst)):
                    result.append([lst[p1],lst[p2]])
    return result

def calc_product_correlation(df, prod1, prod2):
	spearmans = []
	prod1_df = get_data_selection(df, products=[prod1])
	prod2_df = get_data_selection(df, products=[prod2])
	countries = overlap_in_countries(prod1_df, prod2_df)
	for country in countries:
		country_prod1_df = get_data_selection(prod1_df, countries=[country])
		country_prod2_df = get_data_selection(prod2_df, countries=[country])
		years = overlap_in_years(country_prod1_df, country_prod2_df)
		if(len(years) > 4):
			year_prod1_df = get_data_selection(country_prod1_df, years=years)
			year_prod2_df = get_data_selection(country_prod2_df, years=years)
			spearman, p_value = spearmanr(year_prod1_df['price_change'], year_prod2_df['price_change'])
			if(p_value <=0.05 and not(isnan(spearman))):
				spearmans.append(spearman)
	# print(spearmans)
	return np.mean(spearmans)

if __name__ == '__main__':
	price_df = load_price_data()	
	data = []
	combos = all_combinations(price_df._product.unique().tolist())
	x = 0
	size = len(combos)
	for combo in combos:
		if(x % 100 == 0):
			print("{}/{}".format(x, size))
		avg_spearman = calc_product_correlation(price_df, combo[0], combo[1])
		if(not isnan(avg_spearman)):
			data.append((combo, avg_spearman))
		x = x + 1

	print("write to file...")
	with open('product_correlations4.csv','wb') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['combo','spearman'])
	    for row in data:
	        csv_out.writerow(row)

	# print(calc_product_correlation(price_df, "Bread", "Wheat"))
