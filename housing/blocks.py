import geopandas as gpd

df = gpd.read_file('./tl_2020_36_tabblock20.zip')
df = df[df.COUNTYFP20 == '067']
df.to_file('census-2020-blocks-onon067.json', driver='GeoJSON')