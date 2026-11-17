import geopandas as gpd

df = gpd.read_file('./tl_2020_36_tract.zip')
df = df[df.COUNTYFP == '067']
df.to_file('census-2020-tracts-onon067.json', driver='GeoJSON')