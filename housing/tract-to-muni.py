import geopandas as gpd
import requests

### Get city/town boundaries (does not include villages)
url = 'https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Civil_Boundaries/FeatureServer/6/query'
params = {
  'f': 'json',
  'where': "county='Onondaga'",
  'outFields': 'NAME'
}

munis = requests.get(url, params)
munis = gpd.read_file(munis.text)
munis = munis.to_crs(4269)

### Import tracts
tracts = gpd.read_file('./census-2020-tracts-onon067.json')
tracts = tracts.to_crs(4269)

### Use the centroid for merging
tracts['centroid_geom'] = tracts.geometry.centroid
tracts['poly_geom'] = tracts.geometry
tracts = tracts.set_geometry('centroid_geom')

### Merge the two layers
merged = tracts.sjoin(munis)#, how="inner", predicate='intersects')#, how='left')#, predicate='intersects')
merged = merged.rename(columns={'NAME_left': 'tract_name', 'NAME_right': 'muni_name'})

### Restore original geometry to tracts
merged = merged.set_geometry('poly_geom')

### Output the merged tracts-municipalities
merged[['tract_name', 'muni_name']].to_csv('../../../../../../Downloads/tracts-munis.csv')

# Original problem tracts :::::
#        NAME                                           geometry
# 10      154  POLYGON ((-76.0407 43.09494, -76.03816 43.0950...
# 25      129  POLYGON ((-76.23156 43.06862, -76.23107 43.068...
# 26      130  POLYGON ((-76.23084 43.0572, -76.23075 43.0572...
# 28   165.02  POLYGON ((-76.36989 43.01058, -76.35554 43.011...
# 56      107  POLYGON ((-76.12981 43.14488, -76.12958 43.144...
# 57      108  POLYGON ((-76.14861 43.13882, -76.1467 43.1388...
# 75      122  POLYGON ((-76.31778 43.03895, -76.31737 43.039...
# 78      117  POLYGON ((-76.36281 43.16168, -76.3627 43.1617...
# 79      133  POLYGON ((-76.22265 43.10779, -76.22257 43.107...
# 97      143  POLYGON ((-76.09016 43.06741, -76.09 43.06743,...
# 120     116  POLYGON ((-76.36458 43.16612, -76.3645 43.1667... LYSANDER
# 124  152.02  POLYGON ((-75.97674 43.02426, -75.9744 43.0237... MANLIUS