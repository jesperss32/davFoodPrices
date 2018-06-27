import pandas as pd
import numpy as np
import csv
from df_functions import regions, get_data_selection, load_price_data, overlap_in_years, overlap_in_markets
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
	markets = overlap_in_markets(prod1_df, prod2_df)
	for market in markets:
		market_prod1_df = get_data_selection(prod1_df, markets=[market])
		market_prod2_df = get_data_selection(prod2_df, markets=[market])
		years = overlap_in_years(market_prod1_df, market_prod2_df)
		if(len(years) > 4):
			# print(years)
			year_prod1_df = get_data_selection(market_prod1_df, years=years)
			year_prod2_df = get_data_selection(market_prod2_df, years=years)
			# print("({}, {}): {}".format(prod1, prod2, country))
			spearman, p_value = spearmanr(year_prod1_df['price_change'], year_prod2_df['price_change'])
			if(p_value <= 0.05 and not(isnan(spearman))):
				spearmans.append(spearman)
	# print(spearmans)
	return np.mean(spearmans)

if __name__ == '__main__':
	europe, middle_east, asia, africa = regions()
	price_df = pd.read_csv('../data/fooddatasets/only_complete_years_data_percentages.csv')	
	price_df = get_data_selection(price_df, countries = africa)
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
	with open('product_correlations_monthly_minimal_5yrs_africa.csv','wb') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['combo','spearman'])
	    for row in data:
	        csv_out.writerow(row)


	# print(calc_product_correlation(price_df, "Bread", "Wheat"))
