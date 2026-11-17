import geopandas as gpd
import requests

### Get the municipal boundaries
url = 'https://spatialags.vhb.com/arcgis/rest/services/29821_Syr_Onondaga/Layers_2022/MapServer/2/query'
params = {
  'f': 'pjson',
  'where': '1=1',
  'outFields': '*'
}

munis = requests.get(url, params)
munis = gpd.read_file(munis.text)
munis = munis.to_crs(4269)

### Import blocks
blocks = gpd.read_file('./census-2020-blocks-onon067.json')

### Try to merge the two layers
merged = blocks.sjoin(munis, predicate='within')
# blocks are within munis

merged.to_file('within.json', driver='GeoJSON')

print(merged)