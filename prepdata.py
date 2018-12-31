#
# download 'parsed_all_phishing.csv' from https://drive.google.com/file/d/1oDMwaMXLU9lbzd2EXd07AR2Rt_aJX9jt/view?usp=sharing
#

import pandas as pd
import numpy as np

# set pandas output width
desired_width = 320
pd.set_option('display.width', desired_width)

# read dataset
path = 'parsed_all_phishing.csv'
fields = ['country']
df = pd.read_csv(path, usecols=fields, na_filter = False)
df['country'] = df['country'].str.upper()

path2 = 'convertcsv.csv'
fields2 = ['#ISO', 'Country', 'Continent','Population']
df2 = pd.read_csv(path2, usecols=fields2, na_filter = False)

# count phishing sites per country
dictt = {}
for row in df.itertuples(index=True, name='Pandas'):
	c = getattr(row, 'country')
	if c not in dictt.keys():
		dictt[c] = 1
	else:
		dictt[c] = dictt[c] + 1

# write countrycode, country, population and no of phishing sites to csv file
with open('temp.csv', 'w') as file:
	file.write('countrycode,country,continent,population,phishingsites\n')
	for countrycode in dictt.keys():
		if countrycode in df2['#ISO'].values:
			country = str(df2['Country'][df2.loc[df2['#ISO']==countrycode].index[0]]) # ugly way to find country by row index
			continent = str(df2['Continent'][df2.loc[df2['#ISO']==countrycode].index[0]]) # ugly way to find continent by row index
			population = str(df2['Population'][df2.loc[df2['#ISO']==countrycode].index[0]]) # ugly way to find population by row index
			phishingsites = str(dictt[countrycode])

			string = countrycode + ',' + country + ','  + continent + ',' + population + ',' + phishingsites
			file.write(string)
			file.write('\n')

def divide(a, b):
    if b == 0:
        return np.nan
    else: 
        return (a/b)*1000

# add phishing sites per 1000 citizens column to finalize
df3 = pd.read_csv('temp.csv', na_filter=False)
df3['ratio'] = df3.apply(lambda row: divide(row.phishingsites, row.population), axis=1)
with open('final.csv', 'w') as f:
	df3.to_csv(f)