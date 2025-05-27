import pandas as pd
import requests

companies = [
  'Ithacor Capital',
  'Ithacor Capital Holding1',
  'Ithacor Management',
  'Ithacor Properties',
  'Skodzinsky Real Estate'
]

url = 'https://services2.arcgis.com/fRWb1mz1huf3Aqyy/arcgis/rest/services/Parcel_Viewer_WFL1/FeatureServer/2/query'
params = {
  'f': 'json',
  'where': ' OR '.join(["owner_name LIKE '%s%%'" % c for c in companies]),
  'returnGeometry': False,
  'outFields': '*'
}

r = requests.get(url, params=params)
r = r.json()
r = [feature['attributes'] for feature in r['features']]

df = pd.DataFrame.from_dict(r)
print(df)