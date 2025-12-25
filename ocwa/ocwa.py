import geopandas as gpd
import requests

### Import municipalities
munis = requests.get(
  'https://spatialags.vhb.com/arcgis/rest/services/29821_Syr_Onondaga/Layers_2022/MapServer/2/query',
  params={
    'where': '1=1',
    'outSR': '4326',
    'outFields': '*',
    'f': 'geojson'
  }
)

munis = munis.json()
munis = gpd.GeoDataFrame.from_features(munis, crs='EPSG:4326')

munis = munis[munis.MUNI.isin([
  'Dewitt',
  'Manlius', 'Village of Fayetteville', 'Village of Manlius', 'Village of Minoa',
  'Pompey'
])]

### Import water systems
water = requests.get(
  'https://gisservices.dec.ny.gov/arcgis/rest/services/der/der_viewer/MapServer/4/query',
  params={
    'where': "PRINCIPAL_COUNTY_SERVED='ONONDAGA'",
    'outSR': '4326',
    'outFields': '*',
    'f': 'geojson'
  }
)

water = water.json()
water = gpd.GeoDataFrame.from_features(water, crs='EPSG:4326')

### Join municipalities, water systems; save result
muniswater = water.overlay(munis, how='intersection')
gpd.GeoSeries([muniswater.unary_union]).to_file('muniswater.json', driver='GeoJSON')