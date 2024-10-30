import geopandas as gpd
import pandas as pd
import requests

### Import counties
counties = 'https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Civil_Boundaries/FeatureServer/3/query?where=1%3D1&outSR=4326&f=geojson'
counties = requests.get(counties)
counties = counties.json()
counties = gpd.GeoDataFrame.from_features(counties, crs='EPSG:4326')

### Import districts
CHAMBERS = ['C', 'SA', 'SS']
districts = pd.DataFrame()

for chamber in CHAMBERS:
  file_districts = gpd.read_file('./ny-%s.geojson' % chamber.lower())
  file_districts['chamber'] = chamber
  districts = pd.concat([districts, file_districts[['NAME', 'chamber', 'geometry']]])

### Merge counties, selected districts
SELETED_DISTRICTS = [
  { 'chamber': 'C', 'number': '22' },
  { 'chamber': 'C', 'number': '24' },
  { 'chamber': 'SS', 'number': '48' },
  { 'chamber': 'SS', 'number': '50' }
]

for selected_district in SELETED_DISTRICTS:
  district = districts[
    (districts.chamber == selected_district['chamber']) &
    (districts.NAME == selected_district['number'])
  ]
  result = gpd.overlay(district, counties)

  result = result[['NAME_2', 'geometry']]
  result = result.rename(columns={'NAME_2': 'name'})
  result['name'] = result.name.str.capitalize() + ' County'

  filename = 'dist-%s-%s.geojson' % (selected_district['chamber'], selected_district['number'])
  result.to_file(filename, driver='GeoJSON')