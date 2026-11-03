const { center: turfCenter, feature: turfFeature } = require('@turf/turf');
const { writeFile } = require('fs/promises');

return fetch('https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Civil_Boundaries/FeatureServer/3/query?where=1%3D1&outSR=4326&f=geojson')
  .then(r => r.json())
  .then(r => Promise.resolve(r.features))
  .then((features) => {
    return Promise.all(features.map((feature) => {
      const centroid = turfCenter(turfFeature(feature.geometry)).geometry.coordinates;

      return Promise.resolve({
        county: feature.properties.NAME,
        lat: centroid[1],
        lon: centroid[0]
      });
    }));
  })
  .then((features) => {
    return writeFile(`./ny-county-centroids.json`, JSON.stringify(features));
  });