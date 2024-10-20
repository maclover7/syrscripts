import geopandas as gpd
import requests

### Import counties
counties = 'https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Civil_Boundaries/FeatureServer/2/query?where=1%3D1&outSR=4326&f=geojson'
counties = requests.get(counties)
counties = counties.json()
counties = gpd.GeoDataFrame.from_features(counties, crs='EPSG:4326')

### Import congressional districts
districts = gpd.read_file('./ny-c.geojson')
districts = districts[['NAME', 'geometry']]

### Merge counties, selected districts
SELETED_DISTRICTS = [{ 'type': 'C', 'number': '22' }, { 'type': 'C', 'number': '24' }]
for selected_district in SELETED_DISTRICTS:
  district = districts[districts.NAME == selected_district['number']]
  result = gpd.overlay(district, counties)

  result = result[['NAME_2', 'geometry']]
  result = result.rename(columns={'NAME_2': 'name'})
  result['name'] = result.name.str.capitalize() + ' County'

  filename = 'dist-%s-%s.geojson' % (selected_district['type'], selected_district['number'])
  result.to_file(filename, driver='GeoJSON')