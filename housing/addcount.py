import pandas as pd
import requests
from io import StringIO

# BPS data is from https://socds.huduser.gov/permits/
# diff_bps is "Monthly Final" for the sum of Onondaga County
df = pd.DataFrame([
  ['2023-july', pd.NA, pd.NA, 157, 'https://www2.census.gov/geo/pvs/addcountlisting/2023/36_NewYork_AddressBlockCountList_072023.txt'],
  ['2023-dec', pd.NA, pd.NA, 154, 'https://www2.census.gov/geo/pvs/addcountlisting/2023/36_NewYork_AddressBlockCountList_122023.txt'],
  ['2024-july', pd.NA, pd.NA, 256, 'https://www2.census.gov/geo/pvs/addcountlisting/2024/36_NewYork_AddressBlockCountList_072024.txt'],
  ['2024-dec', pd.NA, pd.NA, 359, 'https://www2.census.gov/geo/pvs/addcountlisting/2024/36_NewYork_AddressBlockCountList_122024.txt'],
  ['2025-july', pd.NA, pd.NA, 191, 'https://www2.census.gov/geo/pvs/addcountlisting/2025/36_NewYork_AddressBlockCountList_072025.txt'],
  ['2025-dec', pd.NA, pd.NA, 1570, 'https://www2.census.gov/geo/pvs/addcountlisting/2025/36_NewYork_AddressBlockCountList_122025.txt']
], columns=['release_date', 'total_housing', 'total_groupquarters', 'diff_bps', 'url'])

for (index, row) in df.iterrows():
  releasereq = requests.get(row.url).content
  releasereq = StringIO(str(releasereq, 'utf-8'))
  releasedf = pd.read_csv(releasereq, sep='|')

  releasedf = releasedf[(releasedf.STATE == 36) & (releasedf.COUNTY == 67)]

  df.loc[index, 'total_housing'] = releasedf['TOTAL HOUSING UNITS'].sum()
  df.loc[index, 'total_groupquarters'] = releasedf['TOTAL GROUP QUARTERS'].sum()

df['diff_housing'] = df[['total_housing']].diff()
df = df.drop(['total_groupquarters', 'url'], axis=1)

print(df)