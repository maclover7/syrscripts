import pandas as pd

### Set race
RACE_TO_PROCESS = 'gov'

### Import data
centroidsdf = pd.read_json('ny-county-centroids.json')
resultsdf = pd.read_json('ny-county-results-%s.json' % RACE_TO_PROCESS, orient='records').reset_index()

### Prepare county results, then match with centroids
resultsdf = resultsdf.rename(columns={'countyName': 'county'})
resultsdf['county'] = resultsdf.county.replace('St.Lawrence', 'St Lawrence')
resultsdf = pd.merge(resultsdf, centroidsdf, on='county')

### Properly format results
resultsdf['demvote'] = resultsdf['candidates'][0][0]['votes']
resultsdf['dempct'] = resultsdf['candidates'][0][0]['pct']

resultsdf['repvote'] = resultsdf['candidates'][0][1]['votes']
resultsdf['reppct'] = resultsdf['candidates'][0][1]['pct']

resultsdf['wivote'] = resultsdf['candidates'][0][2]['pct']
resultsdf['wipct'] = resultsdf['candidates'][0][2]['pct']

resultsdf = resultsdf.drop('candidates', axis=1)

### Set winner attributes
def calculate_winner_party(x):
    if x.demvote > x.repvote:
        return 'Democrat'
    else:
        return 'Republican'

def calculate_winner_margin(x):
    if x.winnerparty == 'Democrat':
        return x.demvote - x.repvote - x.wivote
    else:
        return x.repvote - x.demvote - x.wivote

resultsdf['winnerparty'] = resultsdf.apply(calculate_winner_party, axis=1)
resultsdf['winnermargin'] = resultsdf.apply(calculate_winner_margin, axis=1)

resultsdf[[
    'county', 'lat', 'lon',
    'demvote', 'dempct', 'repvote', 'reppct',
    'winnermargin', 'winnerparty'
]].to_csv('./ny-county-results-%s.csv' % RACE_TO_PROCESS, index=False)

### Refine further for upstate/downstate analysis
REGION_DOWNSTATE = [
    'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
    'Nassau', 'Suffolk',
    'Westchester'
]

resultsdf['region'] = resultsdf.apply(lambda x: 'Downstate' if x['county'] in REGION_DOWNSTATE else 'Upstate', axis=1)

regionresultsdf = resultsdf.groupby('region').agg({
    'demvote': sum,
    'repvote': sum,
    'wivote': sum
}).reset_index()
regionresultsdf['dempct'] = 100 * regionresultsdf.demvote / regionresultsdf.sum(axis=1, numeric_only=True)
regionresultsdf['reppct'] = 100 * regionresultsdf.repvote / regionresultsdf.sum(axis=1, numeric_only=True)

print(regionresultsdf)