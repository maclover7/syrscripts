import json
import pandas as pd

### Set race
RACE_TO_PROCESS = 'comp'

### Import data
centroidsdf = pd.read_json('ny-county-centroids.json')

resultspredf = []
with open('ny-county-results-%s.json' % RACE_TO_PROCESS) as f:
    counties = json.load(f)
    for county in counties:
        resultspredf.append([
            county['countyName'],
            county['candidates'][0]['votes'],
            county['candidates'][0]['pct'],
            county['candidates'][1]['votes'],
            county['candidates'][1]['pct'],
            county['candidates'][2]['votes'],
            county['candidates'][2]['pct'],
        ])

resultsdf = pd.DataFrame(resultspredf, columns=['county', 'demvote', 'dempct', 'repvote', 'reppct', 'wivote', 'wipct'])

### Prepare county results, then match with centroids
resultsdf = resultsdf.rename(columns={'countyName': 'county'})
resultsdf['county'] = resultsdf.county.replace('St.Lawrence', 'St Lawrence')
resultsdf = pd.merge(resultsdf, centroidsdf, on='county')

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
regionresultsdf['wipct'] = 100 * regionresultsdf.wivote / regionresultsdf.sum(axis=1, numeric_only=True)

print(regionresultsdf)