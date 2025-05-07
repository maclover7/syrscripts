import requests
import pandas as pd

df = pd.DataFrame([], columns=['height', 'time'])

for year in range(2014, 2026):
  req = requests.get('https://nwis.waterservices.usgs.gov/nwis/iv/', params={
    'agencyCd': 'USGS',
    'endDt': '%i-12-31T23:59:59.999-04:00' % year,
    'format': 'json',
    'parameterCd': '00065',
    'sites': '04236800',
    'startDt': '%i-01-01T00:00:00.000-04:00' % year
  })
  req = req.json()

  yeardf = pd.DataFrame(req['value']['timeSeries'][0]['values'][0]['value'])
  yeardf = yeardf[['value', 'dateTime']]
  yeardf = yeardf.rename(columns={'value': 'height', 'dateTime': 'time'})
  yeardf['time'] = pd.to_datetime(yeardf.time)
  df = pd.concat([df, yeardf])

df['date'] = df['time'].dt.date
df.groupby('date').max()[['height']].to_csv('heights-max-day.csv')
df.to_csv('heights.csv', index=False)