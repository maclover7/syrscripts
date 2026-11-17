import pandas as pd
import requests
from io import StringIO

def get_census_data(path, column_name):
    req = requests.get('https://www2.census.gov/geo/pvs/addcountlisting/%s' % path).content
    req = StringIO(str(req, 'utf-8'))

    df = pd.read_csv(req, sep='|')
    df = df[(df.STATE == 36) & (df.COUNTY == 67)]

    dfagg = df.groupby(by='TRACT')['TOTAL HOUSING UNITS'].sum().reset_index()
    return dfagg.rename(columns={'TRACT': 'tract_name', 'TOTAL HOUSING UNITS': column_name})

df20 = get_census_data('2020/36_NewYork_AddressBlockCountList_062022.txt', '2020_census')
df25dec = get_census_data('2025/36_NewYork_AddressBlockCountList_122025.txt', '2025_dec')

df = pd.merge(df20, df25dec, on='tract_name')
df['pctdiff'] = 100 * (df['2025_dec'] - df['2020_census']) / df['2020_census']

dftracts = pd.read_csv('../../../../../../Downloads/tracts-munis.csv')
df = pd.merge(df, dftracts, on='tract_name')

dfmunis = df.groupby(by='muni_name').agg({ '2020_census': 'sum', '2025_dec': 'sum' }).reset_index()
dfmunis['pctdiff'] = 100 * (dfmunis['2025_dec'] - dfmunis['2020_census']) / dfmunis['2020_census']

df.to_csv('../../../../../../Downloads/tracts-housing.csv')
dfmunis.to_csv('../../../../../../Downloads/munis-housing.csv')