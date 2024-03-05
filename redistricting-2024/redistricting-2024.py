import geopandas as gpd
import pandas as pd

### Import cervas plan
cervasplan = gpd.read_file('redistricting-2024/plan-cervas.geojson')
cervasplan = cervasplan[['NAME', 'geometry']]
cervasplan = cervasplan[cervasplan.NAME == '22']
cervasplan['NAME'] = 'Old-22'

### Import new plan
newplan = gpd.read_file('redistricting-2024/plan-irc.zip')
newplan = newplan.to_crs(4326)
newplan = newplan[['DISTRICT', 'geometry']]
newplan = newplan.rename(columns={'DISTRICT': 'NAME'})
newplan = newplan[newplan.NAME == '22']
newplan['NAME'] = 'New-22'

### Compare, export features
cervasplandist = cervasplan[cervasplan.NAME == 'Old-22']
newplandist = newplan[newplan.NAME == 'New-22']

geoms = [
  cervasplandist.intersection(newplandist.unary_union),
  cervasplandist.difference(newplandist.unary_union),
  newplandist.difference(cervasplandist.unary_union)
]
geoms = map(lambda x: gpd.GeoDataFrame(geometry=x.geometry), geoms)
geoms = gpd.GeoDataFrame(pd.concat(geoms))
geoms['NAME'] = ['union', 'cervasplanonly', 'newplanonly']

geoms.to_file('redistricting-2024/out-diff.geojson', driver='GeoJSON')